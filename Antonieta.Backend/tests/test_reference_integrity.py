from datetime import datetime
from support import DatabaseTestCase


class ReferenceIntegrityTests(DatabaseTestCase):
    def test_cannot_delete_stock_with_movements(self):
        stock = self.stock()
        self.request('POST', '/ration-input/', json={
            'ration_stock_id': stock, 'amount': 5,
            'date': datetime.now().isoformat(), 'description': 'Donation',
        })
        response = self.request('DELETE', f'/ration-stock/{stock}')
        self.assertEqual(response.status_code, 409, response.text)
        self.assertEqual(self.balance(stock), 105)

    def test_cannot_delete_beneficiary_with_distributions(self):
        person = self.beneficiary()
        self.request('POST', '/distribution/', json={
            'ration_id': self.stock(), 'beneficiary_id': person, 'amount': 5,
            'date': datetime.now().isoformat(),
        })
        self.assertEqual(self.request('DELETE', f'/beneficiary/{person}').status_code, 409)
        self.assertEqual(self.request('GET', f'/beneficiary/{person}').status_code, 200)

    def test_duplicate_stock_name_returns_safe_conflict(self):
        self.stock()
        response = self.request('POST', '/ration-stock/', json={
            'name': 'Test ration', 'description': 'Test', 'unit': 'kg', 'stock': 100,
        })
        self.assertEqual(response.status_code, 409, response.text)
        self.assertNotIn('INSERT INTO', response.text)
