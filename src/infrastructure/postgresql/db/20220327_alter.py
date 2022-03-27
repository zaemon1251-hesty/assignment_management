from sqlalchemy import Column, DateTime
import sys
import os
sys.path.append("/var/www")


def add_column(engine, column: Column, table):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute('ALTER TABLE %s ADD COLUMN %s %s' %
                   (table.__tablename__, column_name, column_type))


if __name__ == "__main__":
    from src.infrastructure.postgresql.assignments import AssignmentOrm
    from src.infrastructure.postgresql.database import engine

    end_at = Column("end_at", DateTime, default=None)
    add_column(engine, end_at, AssignmentOrm)
