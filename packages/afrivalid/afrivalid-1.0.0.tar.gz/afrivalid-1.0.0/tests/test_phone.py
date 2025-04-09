import unittest
from validator.zw.phone import PhoneNumberValidator

class TestPhoneNumberValidator(unittest.TestCase):
    def setUp(self):
        self.validator = PhoneNumberValidator()

    def test_econet_valid(self):
        result = self.validator.validate("0771234567")
        self.assertTrue(result['econet'])

    def test_netone_invalid(self):
        result = self.validator.validate("0811234567")
        self.assertFalse(result['netone'])

    def test_invalid_phone(self):
        result = self.validator.validate("0000000000")
        self.assertFalse(result['valid'])

if __name__ == "__main__":
    unittest.main()
