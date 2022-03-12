###
from .conf import DOMAINS


class TargetNotFoundException(Exception):
    """存在するはずのターゲットが存在しない際の例外"""
    domain: DOMAINS

    def __init__(self, message, domain: DOMAINS, *args, **kwargs):
        self.domain = domain
        message += "\n"
        message += str(domain)
        super().__init__(message)


class TargetAlreadyExsitException(Exception):
    """存在しないはずのターゲットが存在する際の例外"""
    domain: DOMAINS

    def __init__(self, message, domain: DOMAINS, *args, **kwargs):
        self.domain = domain
        message += "\n"
        message += str(domain)
        super().__init__(message)


class UnauthorizedException(Exception):
    """ユーザー認証失敗時の例外"""
    pass


class CredentialsException(Exception):
    """tokenを検証出来ない時の例外"""
    pass
