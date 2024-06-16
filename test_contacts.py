import unittest
from faker_contacts import generate_contacts

class TestContacts(unittest.TestCase):
    def test_generate_contacts(self):
        user_id = 1
        count = 5
        contacts = generate_contacts(user_id, count)
        self.assertEqual(len(contacts), count)

if __name__ == '__main__':
    unittest.main()