from sqlalchemy import or_, and_


def make_conditions(orm, attr, value):
    res = None

    if hasattr(value, "__iter__"):
        or_filters = []
        for v in value:
            or_filters.append(
                and_(
                    getattr(
                        orm,
                        attr) == v))
        res = or_(*or_filters)

    elif attr.split("_")[-1] == "be":
        """[(column_name)_be] という形式の文字列になっているので、_beを取り除くとカラム名が取り出せる"""
        attr = attr[:-3]
        res = and_(
            getattr(
                orm,
                attr) < value)

    elif attr.split("_")[-1] == "af":
        """[(column_name)_af] という形式の文字列になっているので、_afを取り除くとカラム名が取り出せる"""
        attr = attr[:-3]
        res = and_(
            getattr(
                orm,
                attr) > value)

    else:
        res = and_(
            getattr(
                orm,
                attr) == value)

    return res
