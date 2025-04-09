from theaddressor import AddressParser
import unittest
import random

class TestAddressParser(unittest.TestCase):

    def _shuffle_and_parse(self, lines):
        random.shuffle(lines)
        parser = AddressParser(lines)
        return parser.get()

    def assertEqualIgnoreCase(self, a, b):
        self.assertEqual(a.lower(), b.lower())

    def test_multiline_name_and_reference(self):
        lines = [
            "Very Important",
            "Person Inc.",
            "1024 Bitwise Blvd",
            "Suite 204",
            "Silicon Valley, CA 94043",
            "Reference #A1B2C3",
            "vip@vip.com",
            "(650) 555-4321"
        ]
        result = AddressParser(lines).get()
        self.assertEqualIgnoreCase(result['name'], 'Very Important')
        self.assertEqualIgnoreCase(result['address1'], '1024 Bitwise Blvd')
        self.assertEqualIgnoreCase(result['address2'], 'Suite 204')
        self.assertEqualIgnoreCase(result['city'], 'Silicon Valley')
        self.assertEqualIgnoreCase(result['state'], 'CA')
        self.assertEqualIgnoreCase(result['zipcode'], '94043')
        self.assertEqualIgnoreCase(result['reference'][0], 'Reference #A1B2C3')
        self.assertEqualIgnoreCase(result['email'][0], 'vip@vip.com')
        self.assertEqualIgnoreCase(result['phone'][0], '(650) 555-4321')

    def test_weird_formatting_and_symbols(self):
        lines = [
            "*** Acme Rockets ***",
            "#500 Rocket Rd",
            "Area 51, NV 88901",
            "Contact: acme@rockets.com",
            "Tel: 702.555.9999"
        ]
        result = AddressParser(lines).get()
        self.assertEqualIgnoreCase(result['name'], '*** Acme Rockets ***')
        self.assertEqualIgnoreCase(result['address1'], '#500 Rocket Rd')
        self.assertEqualIgnoreCase(result['city'], 'Area 51')
        self.assertEqualIgnoreCase(result['state'], 'NV')
        self.assertEqualIgnoreCase(result['zipcode'], '88901')
        self.assertEqualIgnoreCase(result['email'][0], 'acme@rockets.com')
        self.assertEqualIgnoreCase(result['phone'][0], '702.555.9999')

    def test_canadian_zip_without_spaces(self):
        lines = [
            "Canadian Office",
            "33 Maple Leaf Rd",
            "Ottawa ON K1A0B1"
        ]
        result = AddressParser(lines).get()
        self.assertEqualIgnoreCase(result['country'], 'Canada')
        self.assertEqualIgnoreCase(result['zipcode'], 'K1A0B1')
        self.assertEqualIgnoreCase(result['city'], 'Ottawa')
        self.assertEqualIgnoreCase(result['state'], 'ON')

    def test_multiple_zips_only_one_valid(self):
        lines = [
            "Fake Co",
            "999 Nowhere St",
            "Gotham, NY 99999",
            "Alt zip: 12345678",
            "info@fake.co",
            "(212) 000-0000"
        ]
        result = AddressParser(lines).get()
        self.assertEqualIgnoreCase(result['zipcode'], '99999')
        self.assertEqualIgnoreCase(result['state'], 'NY')
        self.assertEqualIgnoreCase(result['city'], 'Gotham')

    def test_fuzzy_input_with_address_first(self):
        lines = [
            "48 Innovation Way",
            "DeepMind HQ",
            "Suite B",
            "London ON N6A 3K7",
            "contact@deep.ai",
            "(519) 555-0188",
            "Order #X123"
        ]
        result = AddressParser(lines).get()
        self.assertEqualIgnoreCase(result['name'], 'DeepMind HQ')
        self.assertEqualIgnoreCase(result['address1'], '48 Innovation Way')
        self.assertEqualIgnoreCase(result['address2'], 'Suite B')
        self.assertEqualIgnoreCase(result['zipcode'], 'N6A3K7')
        self.assertEqualIgnoreCase(result['reference'][0], 'Order #X123')

    def test_address_with_highway(self):
        lines = [
            "Truck Stop Inc.",
            "I-95 North Exit 42",
            "Fuelville, NC 27501"
        ]
        result = AddressParser(lines).get()
        self.assertEqualIgnoreCase(result['address1'], 'I-95 North Exit 42')
        self.assertEqualIgnoreCase(result['city'], 'Fuelville')
        self.assertEqualIgnoreCase(result['state'], 'NC')
        self.assertEqualIgnoreCase(result['zipcode'], '27501')

    def test_address_with_state_named_street(self):
        lines = [
            "Texas BBQ Co.",
            "101 Texas Ave",
            "Austin TX 73301"
        ]
        result = AddressParser(lines).get()
        self.assertEqualIgnoreCase(result['address1'], '101 Texas Ave')
        self.assertEqualIgnoreCase(result['city'], 'Austin')
        self.assertEqualIgnoreCase(result['state'], 'TX')
        self.assertEqualIgnoreCase(result['zipcode'], '73301')

    def test_suite_inline_with_address(self):
        lines = [
            "StartUp Co",
            "88 Founders St Suite 101",
            "Palo Alto CA 94301"
        ]
        result = AddressParser(lines).get()
        self.assertTrue("suite" in result['address1'].lower() or result['address2'])

    def test_url_tag_does_not_crash(self):
        lines = [
            "Cool Company",
            "44 Edge Case Rd",
            "Testville TX 75001",
            "https://orders.coolco.com?id=123"
        ]
        result = AddressParser(lines).get()
        self.assertTrue(result['url'][0].startswith('https://'))

    def test_name_with_initials_and_suffix(self):
        lines = [
            "Dr. J. D. Smith Jr.",
            "12 Lab Ln",
            "Bio City, CA 90001"
        ]
        result = AddressParser(lines).get()
        self.assertEqualIgnoreCase(result['name'], 'Dr. J. D. Smith Jr.')
        self.assertEqualIgnoreCase(result['address1'], '12 Lab Ln')

    def test_address_with_no_suffix(self):
        lines = [
            "Somewhere Inc.",
            "777 Foo",
            "Bar City, FL 32100"
        ]
        result = AddressParser(lines).get()
        self.assertEqualIgnoreCase(result['address1'], '777 Foo')
        self.assertEqualIgnoreCase(result['city'], 'Bar City')
        self.assertEqualIgnoreCase(result['state'], 'FL')
        self.assertEqualIgnoreCase(result['zipcode'], '32100')

    def test_split_canadian_zip_parts(self):
        lines = [
            "Maple Inc.",
            "22 Iceberg Rd",
            "Toronto ON",
            "M4B",
            "1B3"
        ]
        result = AddressParser(lines).get()
        self.assertEqualIgnoreCase(result['zipcode'], 'M4B1B3')
        self.assertEqualIgnoreCase(result['country'], 'Canada')


if __name__ == '__main__':
    unittest.main()    # === New Tests for Edge Cases ===
