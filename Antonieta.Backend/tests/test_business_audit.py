from datetime import datetime
from unittest.mock import patch
from support import DatabaseTestCase
from models.audit_log_model import AuditLog
from models.beneficiary_model import Beneficiary


class BusinessAuditTests(DatabaseTestCase):
    def test_business_mutations_record_actor_and_entity(self):
        stock = self.stock()
        person = self.beneficiary()
        record = self.request('GET', f'/beneficiary/{person}').json()
        response = self.request('PUT', '/beneficiary/', json={**record, 'name': 'Changed person'})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(self.request('DELETE', f'/beneficiary/{person}').status_code, 200)
        with self.sessions() as db:
            logs = db.query(AuditLog).all()
            actions = {(row.entity_type, row.action) for row in logs}
            self.assertTrue({('RationStock', 'CREATE'), ('Beneficiary', 'CREATE'),
                             ('Beneficiary', 'UPDATE'), ('Beneficiary', 'DELETE')} <= actions)
            self.assertTrue(all(row.user_id == 2 for row in logs))
            self.assertTrue(all(row.ip_address for row in logs))
            self.assertNotIn('12345678900', str([row.changes for row in logs]))
            self.assertNotIn('Changed person', str([row.changes for row in logs]))

    def test_stock_movements_are_audited(self):
        stock = self.stock()
        person = self.beneficiary()
        data = {'ration_stock_id': stock, 'amount': 5, 'date': datetime.now().isoformat(), 'description': 'Donation'}
        created = self.request('POST', '/ration-input/', json=data).json()
        self.request('PUT', f"/ration-input/{created['id']}", json={**data, 'id': created['id'], 'amount': 6})
        self.request('DELETE', f"/ration-input/{created['id']}")
        distribution = self.request('POST', '/distribution/', json={
            'ration_id': stock, 'beneficiary_id': person, 'amount': 3, 'date': data['date'],
        }).json()
        self.request('PUT', f"/distribution/{distribution['id']}", json={**distribution, 'amount': 2})
        self.request('DELETE', f"/distribution/{distribution['id']}")
        with self.sessions() as db:
            for entity in ('RationInput', 'Distribution'):
                self.assertEqual({row.action for row in db.query(AuditLog).filter_by(entity_type=entity)},
                                 {'CREATE', 'UPDATE', 'DELETE'})

    def test_beneficiary_logs_do_not_contain_personal_data(self):
        with self.assertLogs('controllers.beneficiary_controller', level='DEBUG') as logs:
            self.beneficiary()
        self.assertNotIn('12345678900', '\n'.join(logs.output))
        self.assertNotIn('Test Person', '\n'.join(logs.output))

    def test_audit_failure_rolls_back_stock_and_movement(self):
        stock = self.stock()
        with patch('services.transaction_audit.record_change', side_effect=RuntimeError('Audit unavailable')):
            with self.assertRaises(RuntimeError):
                self.request('POST', '/ration-input/', json={
                    'ration_stock_id': stock, 'amount': 5,
                    'date': datetime.now().isoformat(), 'description': 'Donation',
                })
        self.assertEqual(self.balance(stock), 100)
        self.assertEqual(self.request('GET', '/ration-input/').json(), [[], 0])
