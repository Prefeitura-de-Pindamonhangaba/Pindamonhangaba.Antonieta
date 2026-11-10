from support import DatabaseTestCase
import unittest
from cors_config import PRODUCTION_ORIGIN, get_cors_origins


class CorsConfigurationTests(unittest.TestCase):
    def test_production_json_array_configuration_is_supported(self):
        self.assertEqual(get_cors_origins(f'["{PRODUCTION_ORIGIN}", "https://staging.example/"]'),
                         [PRODUCTION_ORIGIN, 'https://staging.example'])

    def test_json_wildcard_and_nonstring_entries_are_rejected(self):
        for value in ('["*"]', '[123]', '["https://example.com", null]'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                get_cors_origins(value)

    def test_production_is_allowed_with_legacy_configuration(self):
        self.assertIn(PRODUCTION_ORIGIN, get_cors_origins('http://localhost:3000'))

    def test_missing_configuration_allows_official_site_and_local_development(self):
        self.assertEqual(get_cors_origins(None), [PRODUCTION_ORIGIN, 'http://localhost:3000'])

    def test_normalizes_spaces_trailing_slashes_and_duplicates(self):
        self.assertEqual(get_cors_origins(f' {PRODUCTION_ORIGIN}/, ,{PRODUCTION_ORIGIN} '),
                         [PRODUCTION_ORIGIN])

    def test_explicit_configuration_does_not_add_local_development(self):
        self.assertEqual(get_cors_origins('https://staging.example/'),
                         [PRODUCTION_ORIGIN, 'https://staging.example'])

    def test_wildcard_is_rejected(self):
        with self.assertRaises(ValueError):
            get_cors_origins('http://localhost:3000, *')


class CorsTests(DatabaseTestCase):
    def test_production_origin_can_preflight_login_and_authenticated_requests(self):
        origin = 'https://antonieta.pindamonhangaba.sp.gov.br'
        for path, method in [('/auth/token', 'POST'), ('/beneficiary/', 'GET'),
                             ('/distribution/1', 'PUT')]:
            with self.subTest(path=path):
                response = self.client.options(path, headers={
                    'Origin': origin, 'Access-Control-Request-Method': method,
                    'Access-Control-Request-Headers': 'authorization,content-type',
                })
                self.assertEqual(response.status_code, 200, response.text)
                self.assertEqual(response.headers.get('access-control-allow-origin'), origin)
                self.assertEqual(response.headers.get('access-control-allow-credentials'), 'true')

    def test_production_origin_receives_cors_headers_on_authentication_error(self):
        origin = 'https://antonieta.pindamonhangaba.sp.gov.br'
        response = self.client.get('/beneficiary/', headers={'Origin': origin})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers.get('access-control-allow-origin'), origin)

    def test_cors_only_accepts_configured_origins(self):
        for origin, allowed in [('http://localhost:3000', True), ('https://untrusted.example', False),
                                ('https://antonieta.pindamonhangaba.sp.gov.br.evil.example', False)]:
            with self.subTest(origin=origin):
                response = self.client.options('/beneficiary/', headers={
                    'Origin': origin, 'Access-Control-Request-Method': 'GET',
                    'Access-Control-Request-Headers': 'Authorization',
                })
                self.assertEqual(response.status_code, 200 if allowed else 400)
                self.assertEqual(response.headers.get('access-control-allow-origin'), origin if allowed else None)
