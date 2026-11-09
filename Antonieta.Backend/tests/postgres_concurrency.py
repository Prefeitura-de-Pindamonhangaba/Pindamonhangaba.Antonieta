"""Explicit opt-in: POSTGRES_TEST_URL=... python -m unittest discover -s tests -p postgres_concurrency.py -v."""
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Barrier
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from support import DatabaseTestCase
from main import app
from services.stock_movements import adjust_stock


class PostgresConcurrencyTests(DatabaseTestCase):
    def make_engine(self):
        url = os.environ['POSTGRES_TEST_URL']
        admin = create_engine(url)
        self.addCleanup(admin.dispose)
        schema = 'antonieta_test_' + uuid.uuid4().hex
        with admin.begin() as connection:
            connection.execute(text(f'CREATE SCHEMA {schema}'))

        def cleanup():
            with admin.begin() as connection:
                connection.execute(text(f'DROP SCHEMA {schema} CASCADE'))
        self.addCleanup(cleanup)
        return create_engine(url, connect_args={'options': f'-csearch_path={schema}'})

    def parallel(self, method, path, bodies, module):
        barrier = Barrier(len(bodies), timeout=10)

        def synchronized_adjust(db, deltas):
            barrier.wait()
            return adjust_stock(db, deltas)

        def call(body):
            with TestClient(app) as client:
                return client.request(method, path, headers=self.user, json=body)

        with patch(f'services.{module}.adjust_stock', side_effect=synchronized_adjust):
            with ThreadPoolExecutor(max_workers=len(bodies)) as executor:
                return list(executor.map(call, bodies))

    def test_two_simultaneous_distributions_cannot_spend_same_stock(self):
        stock, person = self.stock(10), self.beneficiary()
        body = {'ration_id': stock, 'beneficiary_id': person, 'amount': 7,
                'date': datetime.now().isoformat()}
        responses = self.parallel('POST', '/distribution/', [body, body], 'distribution_services')
        self.assertEqual(sorted(r.status_code for r in responses), [200, 400])
        self.assertEqual(self.balance(stock), 3)
        self.assertEqual(self.request('GET', '/distribution/').json()[1], 1)

    def test_parallel_inputs_do_not_lose_increments(self):
        stock = self.stock(0)
        body = {'ration_stock_id': stock, 'amount': 2.5, 'date': datetime.now().isoformat(),
                'description': 'Donation'}
        responses = self.parallel('POST', '/ration-input/', [body] * 4, 'ration_input_services')
        self.assertEqual([r.status_code for r in responses], [200] * 4)
        self.assertEqual(self.balance(stock), 10)

    def test_simultaneous_input_removals_cannot_make_stock_negative(self):
        stock = self.stock(0)
        records = []
        for _ in range(2):
            response = self.request('POST', '/ration-input/', json={
                'ration_stock_id': stock, 'amount': 10, 'date': datetime.now().isoformat(),
                'description': 'Donation',
            })
            self.assertEqual(response.status_code, 200, response.text)
            records.append(response.json())
        self.request('POST', '/distribution/', json={
            'ration_id': stock, 'beneficiary_id': self.beneficiary(), 'amount': 10,
            'date': datetime.now().isoformat(),
        })
        # Two independent input records can reach the stock lock concurrently.
        barrier = Barrier(2, timeout=10)
        def adjust(db, deltas):
            barrier.wait()
            return adjust_stock(db, deltas)
        def delete(record):
            with TestClient(app) as client:
                return client.delete(f"/ration-input/{record['id']}", headers=self.user)
        with patch('services.ration_input_services.adjust_stock', side_effect=adjust):
            with ThreadPoolExecutor(max_workers=2) as executor:
                responses = list(executor.map(delete, records))
        self.assertEqual(sorted(r.status_code for r in responses), [200, 400])
        self.assertEqual(self.balance(stock), 0)
