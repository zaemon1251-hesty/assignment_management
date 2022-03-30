from src.usecase.users import UserQueryModel


def process_users_query(q: str = None) -> UserQueryModel:
    query = UserQueryModel()

    for vs in q.split("+"):
        k, v = vs.split("=")
        if k in {'id', 'name', 'email', 'created_at', 'updated_at'}:
            vec = getattr(query, k)
            vec.append(v)
        elif k in {'disabled', 'created_be', 'created_af', 'updated_be', 'updated_af'}:
            setattr(query, k, v)

    return query
