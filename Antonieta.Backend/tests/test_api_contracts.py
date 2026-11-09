from datetime import datetime
from support import DatabaseTestCase


class ApiContractTests(DatabaseTestCase):
    def test_distribution_update_by_route_id(self):
        stock = self.stock()
        record = self.request('POST', '/distribution/', json={
            'ration_id': stock, 'beneficiary_id': self.beneficiary(),
            'amount': 5, 'date': datetime.now().isoformat(),
        }).json()
        response = self.request('PUT', f"/distribution/{record['id']}", json={**record, 'amount': 2.5})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(self.balance(stock), 97.5)

    def test_stock_id_mismatch_rejected(self):
        stock = self.stock()
        record = self.request('GET', f'/ration-stock/{stock}').json()
        response = self.request('PUT', f'/ration-stock/{stock}', json={**record, 'id': 999})
        self.assertEqual(response.status_code, 400, response.text)

    def test_business_missing_resources_return_404(self):
        for path in ('/distribution/999', '/ration-stock/999'):
            with self.subTest(path=path):
                self.assertEqual(self.request('GET', path).status_code, 404)
                self.assertEqual(self.request('DELETE', path).status_code, 404)

    def test_filter_distributions_by_beneficiary(self):
        person = self.beneficiary()
        self.request('POST', '/distribution/', json={
            'ration_id': self.stock(), 'beneficiary_id': person,
            'amount': 2, 'date': datetime.now().isoformat(),
        })
        response = self.request('GET', f'/distribution/beneficiary/{person}')
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()[1], 1)
        self.assertEqual(self.request('GET', '/distribution/beneficiary/999').json(), [[], 0])

    def test_filter_inputs_by_stock(self):
        stock = self.stock()
        self.request('POST', '/ration-input/', json={
            'ration_stock_id': stock, 'amount': 2,
            'date': datetime.now().isoformat(), 'description': 'Donation',
        })
        response = self.request('GET', f'/ration-input/ration-stock/{stock}')
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()[1], 1)

    def test_search_beneficiary_routes(self):
        self.beneficiary()
        for field, value in [('neighborhood', 'Centro'), ('street', 'Test Street')]:
            with self.subTest(field=field):
                response = self.request('GET', f'/beneficiary/search/{field}/{value}')
                self.assertEqual(response.status_code, 200, response.text)
                self.assertEqual(response.json()['total'], 1)
                self.assertEqual(len(response.json()['beneficiaries']), 1)

    def test_report_invalid_month_returns_400(self):
        for report in ('distribution-volume-by-month', 'distribution-summary-by-ration'):
            self.assertEqual(self.request('GET', f'/reports/{report}?month=13').status_code, 400)

