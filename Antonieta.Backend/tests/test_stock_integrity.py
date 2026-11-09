from datetime import datetime
from support import DatabaseTestCase


class StockIntegrityTests(DatabaseTestCase):
    def setUp(self):
        super().setUp()
        self.first = self.stock(100)
        response = self.request('POST', '/ration-stock/', json={
            'name': 'Second ration', 'description': 'Test', 'unit': 'kg', 'stock': 20,
        })
        self.second = response.json()['id']
        self.person = self.beneficiary()
        self.date = datetime.now().isoformat()

    def input(self, amount=10):
        response = self.request('POST', '/ration-input/', json={
            'ration_stock_id': self.first, 'amount': amount,
            'date': self.date, 'description': 'Donation',
        })
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def distribution(self, amount=10):
        response = self.request('POST', '/distribution/', json={
            'ration_id': self.first, 'beneficiary_id': self.person,
            'amount': amount, 'date': self.date, 'observations': 'Keep this',
        })
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def test_input_change_ration_moves_entire_amount_between_stocks(self):
        record = self.input()
        response = self.request('PUT', f"/ration-input/{record['id']}", json={
            **record, 'ration_stock_id': self.second, 'amount': 15.5,
        })
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(self.balance(self.first), 100)
        self.assertEqual(self.balance(self.second), 35.5)

    def test_input_delete_cannot_remove_consumed_stock(self):
        record = self.input()
        self.distribution(110)
        response = self.request('DELETE', f"/ration-input/{record['id']}")
        self.assertEqual(response.status_code, 400, response.text)
        self.assertEqual(self.balance(self.first), 0)
        self.assertEqual(self.request('GET', f"/ration-input/{record['id']}").status_code, 200)

    def test_input_decrease_cannot_remove_consumed_stock(self):
        record = self.input()
        self.distribution(110)
        response = self.request('PUT', f"/ration-input/{record['id']}", json={**record, 'amount': 5})
        self.assertEqual(response.status_code, 400, response.text)
        self.assertEqual(self.balance(self.first), 0)

    def test_input_change_to_missing_stock_rolls_back(self):
        record = self.input()
        response = self.request('PUT', f"/ration-input/{record['id']}", json={
            **record, 'ration_stock_id': 999,
        })
        self.assertEqual(response.status_code, 404, response.text)
        self.assertEqual(self.balance(self.first), 110)

    def test_distribution_change_ration_restores_old_stock_and_debits_new(self):
        record = self.distribution()
        response = self.request('PUT', '/distribution/', json={
            **record, 'ration_id': self.second, 'amount': 12,
        })
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(self.balance(self.first), 100)
        self.assertEqual(self.balance(self.second), 8)

    def test_distribution_change_with_insufficient_stock_rolls_back(self):
        record = self.distribution()
        response = self.request('PUT', '/distribution/', json={
            **record, 'ration_id': self.second, 'amount': 30,
        })
        self.assertEqual(response.status_code, 400, response.text)
        self.assertEqual(self.balance(self.first), 90)
        self.assertEqual(self.balance(self.second), 20)
        self.assertEqual(self.request('GET', f"/distribution/{record['id']}").json()['ration_id'], self.first)

    def test_distribution_edit_accepts_fractional_amount_and_observations(self):
        record = self.distribution()
        response = self.request('PUT', '/distribution/', json={
            **record, 'amount': 5.25, 'observations': 'Updated note',
        })
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()['observations'], 'Updated note')
        self.assertEqual(self.balance(self.first), 94.75)

    def test_invalid_distribution_amounts_rejected(self):
        for amount in (-5, 0, 'NaN', 'Infinity'):
            with self.subTest(amount=amount):
                response = self.request('POST', '/distribution/', json={
                    'ration_id': self.first, 'beneficiary_id': self.person,
                    'amount': amount, 'date': self.date,
                })
                self.assertEqual(response.status_code, 422, response.text)
                self.assertEqual(self.balance(self.first), 100)

    def test_missing_beneficiary_rejected_before_debit(self):
        response = self.request('POST', '/distribution/', json={
            'ration_id': self.first, 'beneficiary_id': 999, 'amount': 5, 'date': self.date,
        })
        self.assertEqual(response.status_code, 404, response.text)
        self.assertEqual(self.balance(self.first), 100)

    def test_negative_direct_stock_update_rejected(self):
        record = self.request('GET', f'/ration-stock/{self.first}').json()
        response = self.request('PUT', f'/ration-stock/{self.first}', json={**record, 'stock': -1})
        self.assertEqual(response.status_code, 422, response.text)
