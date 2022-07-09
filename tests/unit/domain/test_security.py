from unittest import TestCase

from tests.factories import SecurityFactory


class TestSecurity(TestCase):
    def test_extract_ticker_from_name_WHEN_called_with_fii_ticker_on_name_THEN_sets_ticker_on_security(self):
        expected_result = 'BTLG11'
        security = SecurityFactory.build(name='FII BTLG BTLG11 TEST')

        self.assertEqual(expected_result, security.ticker)

    def test_extract_ticker_from_name_WHEN_called_with_fii_ticker_ending_on_b_on_name_THEN_sets_ticker_on_security(self):
        expected_result = 'BTLG11B'
        security = SecurityFactory.build(name='FII BTLG BTLG11B TEST')

        self.assertEqual(expected_result, security.ticker)

    def test_extract_from_name_WHEN_called_with_ticker_without_spaces_THEN_sets_ticker_on_security(self):
        expected_result = 'BTLG11'
        security = SecurityFactory.build(name='FIIBTLGBTLG11TEST')

        self.assertEqual(expected_result, security.ticker)

    def test_extract_ticker_from_name_WHEN_called_with_ordinary_stock_ticker_on_name_THEN_sets_ticker_on_security(self):
        expected_result = 'PETR3'
        security = SecurityFactory.build(name='PETROBRAS ON PETR3 NM')

        self.assertEqual(expected_result, security.ticker)

    def test_extract_ticker_from_name_WHEN_called_with_preferential_stock_ticker_on_name_THEN_sets_ticker_on_security(self):
        expected_result = 'PETR4'
        security = SecurityFactory.build(name='PETROBRAS ON PETR4 NM')

        self.assertEqual(expected_result, security.ticker)

    def test_extract_ticker_from_name_WHEN_called_with_unit_stock_ticker_on_name_THEN_sets_ticker_on_security(self):
        expected_result = 'PETR11'
        security = SecurityFactory.build(name='PETROBRAS ON PETR11 NM')

        self.assertEqual(expected_result, security.ticker)

    def test_extract_ticker_from_name_WHEN_called_with_unit_stock_fraction_ticker_on_name_THEN_sets_ticker_on_security(self):
        expected_result = 'PETR11F'
        security = SecurityFactory.build(name='PETROBRAS ON PETR11F NM')

        self.assertEqual(expected_result, security.ticker)

    def test_extract_ticker_from_name_WHEN_called_with_bdr_ticker_on_name_THEN_sets_ticker_on_security(self):
        expected_result = 'GOOG34'
        security = SecurityFactory.build(name='GOOGLE ON GOOG34 NM')

        self.assertEqual(expected_result, security.ticker)

    def test_extract_ticker_from_name_WHEN_called_with_name_without_ticker_THEN_sets_ticker_as_null(self):
        security = SecurityFactory.build(name='PETROBRAS ON NM')

        self.assertIsNone(security.ticker)