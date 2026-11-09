from support import DatabaseTestCase


class CorsTests(DatabaseTestCase):
    def test_cors_only_accepts_configured_origins(self):
        for origin, allowed in [('http://localhost:3000', True), ('https://untrusted.example', False)]:
            with self.subTest(origin=origin):
                response = self.client.options('/beneficiary/', headers={
                    'Origin': origin, 'Access-Control-Request-Method': 'GET',
                    'Access-Control-Request-Headers': 'Authorization',
                })
                self.assertEqual(response.status_code, 200 if allowed else 400)
                self.assertEqual(response.headers.get('access-control-allow-origin'), origin if allowed else None)
