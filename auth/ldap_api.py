import json
from collections import namedtuple
from typing import Any, Callable, List, NamedTuple, Optional

import ldap3
from ldap3 import Connection, Entry, Server
from ldap3.core.exceptions import LDAPBindError

from auth import cfg

__all__ = ['LdapApi']


class LdapEntry(NamedTuple):
    user_id: str
    surname: str
    full_name: str
    email: str


class LdapApi(object):
    __slots__ = ['_server']

    def __init__(self):
        tls_config = ldap3.Tls(validate=cfg.LDAP3_TLS_VALID,
                               version=cfg.LDAP3_TLS_VERSION)
        self._server: Server = ldap3.Server(host=cfg.LDAP3_HOST,
                                            use_ssl=cfg.LDAP3_USE_SSL,
                                            tls=tls_config,
                                            get_info=ldap3.ALL)

    def validate(self, usr: str, pwd: str):
        try:
            conn = ldap3.Connection(server=self._server,
                                    user=usr,
                                    password=pwd,
                                    version=3,
                                    collect_usage=True,
                                    auto_bind=True)
            conn.unbind()
            return True
        except LDAPBindError:
            return False

    def _exec_context(self, cb: Callable[[Connection], Any]) -> Any:
        with ldap3.Connection(server=self._server,
                              user=cfg.LDAP3_BIND_USR,
                              password=cfg.LDAP3_BIND_PWD,
                              version=3,
                              collect_usage=True,
                              auto_bind=True) as conn:
            res = cb(conn)
        return res

    @staticmethod
    def _entry_parser(entry: Entry) -> LdapEntry:
        dc = json.loads(entry.entry_to_json())['attributes']
        return LdapEntry(user_id=dc['uid'][0],
                         surname=dc['sn'][0],
                         full_name=dc['cn'][0],
                         email=dc['mail'][0])

    def get_entry(self, user_id: str) -> Optional[LdapEntry]:
        def callback(conn: Connection) -> List[Entry]:
            conn.search(
                search_base=cfg.LDAP3_BASE_DN,
                search_filter=cfg.LDAP3_USER_OBJECT_FILTER.format(user_id),
                attributes='*')

            return conn.entries

        entries = self._exec_context(callback)

        try:
            entry = entries[0]
            return self._entry_parser(entry)
        except IndexError:
            return None
