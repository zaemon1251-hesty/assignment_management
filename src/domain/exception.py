###

from src.domain import DOMAINS


class TargetNotFoundException(Exception):
    """ターゲットが存在しない時の例外"""
    domain: DOMAINS

    def __init__(self, message, domain: DOMAINS, *args, **kwargs):
        self.domain = domain
        message += "\n"
        message += str(domain)
        super().__init__(message)


class StateContradictedException(Exception):
    "課題の状態と、提出物の状態が矛盾するときの例外"
    pass
