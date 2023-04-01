import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init():
    global __factory

    if __factory:
        return


    conn_str = ("Driver={SQL Server Native Client 11.0};""Server=DESKTOP-MSI26S3\SQLEXPRESS;"
"Database=web_ws;""Trusted_Connection=yes")

    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": conn_str})
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(connection_url, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
