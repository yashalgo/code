from sqlalchemy import create_engine
from ..common.config import *


def get_sql_engine(db_specs=stocks_data_table):
    engine = create_engine(
        f"postgresql://{db_specs['username']}:{db_specs['password']}@{db_specs['hostname']}/{db_specs['database_name']}"
    )
    return engine
