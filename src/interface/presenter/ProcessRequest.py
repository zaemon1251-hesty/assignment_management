from typing import Any
from src.usecase.users import UserQueryModel
from src.usecase.courses import CourseQueryModel
from src.usecase.assignments import AssignmentQueryModel
from src.usecase.submissions import SubmissionQueryModel


def process_query(q: str, query: Any) -> Any:
    if query is None:
        return None

    QueryMap = {
        "assignment": AssignmentQueryModel(),
        "course": CourseQueryModel(),
        "submission": SubmissionQueryModel()
    }

    for vs in q.split("+"):
        k, v = vs.split("=")
        if k in QueryMap.keys():
            try:
                sub_q = process_query(v, QueryMap.get(k, None))
                setattr(query, k, sub_q)
            except Exception:
                pass
            continue
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
