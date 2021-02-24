import os
import ssl

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # REST
    REST_URL_PREFIX = '/api/v1'
    # LDAP
    LDAP3_TLS_VALID = ssl.CERT_NONE
    LDAP3_TLS_VERSION = None
    LDAP3_HOST = 'ldap.forumsys.com'
    LDAP3_PORT = 389
    LDAP3_BASE_DN = 'dc=example,dc=com'
    LDAP3_USE_SSL = False
    LDAP3_USER_OBJECT_FILTER = "(&(objectClass=inetOrgPerson)(uid={}))"
    LDAP3_ATTRS = ['*']
    LDAP3_TIMEOUT = 10
    LDAP3_CUSTOM_OPTIONS = None
    LDAP3_BIND_USR = 'cn=read-only-admin,dc=example,dc=com'
    LDAP3_BIND_PWD = 'password'


class TestConfig(Config):
    pass
