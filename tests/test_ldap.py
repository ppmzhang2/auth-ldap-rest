import unittest

from auth import cfg
from auth.ldap_api import LdapClient, LdapEntry


class TestLdap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.client = LdapClient()

    def tearDown(self):
        del self.client

    def test_validate(self):
        # correct
        input_1_1 = cfg.LDAP3_BIND_USR
        input_1_2 = cfg.LDAP3_BIND_PWD
        exp_1 = True
        output_1 = self.client.validate(input_1_1, input_1_2)
        self.assertEquals(exp_1, output_1)
        # invalid DN syntax
        input_2_1 = 'no_such_usr'
        input_2_2 = 'no_such_pwd'
        exp_2 = False
        output_2 = self.client.validate(input_2_1, input_2_2)
        self.assertEquals(exp_2, output_2)
        # invalid credentials
        input_3_1 = cfg.LDAP3_BIND_USR
        input_3_2 = 'invalid_password'
        exp_3 = False
        output_3 = self.client.validate(input_3_1, input_3_2)
        self.assertEquals(exp_3, output_3)

    def test_search(self):
        entry_1 = LdapEntry('riemann', 'Riemann', 'Bernhard Riemann',
                            'riemann@ldap.forumsys.com')
        input_1 = entry_1.user_id
        output_1 = self.client.search(input_1)
        entry_2 = None
        input_2 = 'no_such_user'
        output_2 = self.client.search(input_2)
        self.assertEquals(entry_1, output_1)
        self.assertEquals(entry_2, output_2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
