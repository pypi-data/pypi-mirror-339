from enum import Enum


class AdvCheck(str, Enum):
    SSL_HELLO_CHK = "ssl-hello-chk"
    SMTPCHK = "smtpchk"
    LDAP_CHECK = "ldap-check"
    MYSQL_CHECK = "mysql-check"
    PGSQL_CHECK = "pgsql-check"
    TCP_CHECK = "tcp-check"
    REDIS_CHECK = "redis-check"
    HTTPCHK = "httpchk"