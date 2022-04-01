from domain.conf import DOMAINS
from src.usecase.users import UserQueryModel
from usecase.submissions.SubmissionService import SubmissionQueryModel


def process_query(q: str, query: DOMAINS) -> DOMAINS:
    for vs in q.split("+"):
        k, v = vs.split("=")
        attr = getattr(query, k)
        if hasattr(attr, "__iter__"):
            attr.append(v)
        elif attr is not None:
            setattr(query, k, v)
    return query


def process_users_query(q: str = None) -> UserQueryModel:
    return process_query(q, UserQueryModel())


def process_submissions_query(q: str = None) -> SubmissionQueryModel:
    return process_query(q, SubmissionQueryModel())
