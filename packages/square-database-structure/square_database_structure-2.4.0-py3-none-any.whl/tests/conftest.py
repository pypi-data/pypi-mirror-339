import pytest

from square_database_structure.main import global_list_create


def pytest_addoption(parser):
    parser.addoption(
        "--db-host",
        action="store",
        default="raspi.thepmsquare.com",
        help="Database host",
    )
    parser.addoption(
        "--db-port",
        action="store",
        type=int,
        default=15432,
        help="Database port",
    )
    parser.addoption(
        "--db-user",
        action="store",
        default="postgres",
        help="Database user",
    )
    parser.addoption(
        "--db-password",
        action="store",
        default="testing_password",
        help="Database password",
    )


@pytest.fixture(scope="session")
def db_credentials(request):
    return {
        "host": request.config.getoption("--db-host"),
        "port": request.config.getoption("--db-port"),
        "user": request.config.getoption("--db-user"),
        "password": request.config.getoption("--db-password"),
    }


@pytest.fixture(scope="session")
def fixture_create_database_and_tables(db_credentials):
    yield None

    from sqlalchemy import text, create_engine

    local_str_postgres_url = (
        f"postgresql://{db_credentials['user']}:{db_credentials['password']}@"
        f"{db_credentials['host']}:{str(db_credentials['port'])}/"
    )
    postgres_engine = create_engine(local_str_postgres_url)
    with postgres_engine.connect() as postgres_connection:
        postgres_connection.execute(text("commit"))
        for database in global_list_create:
            postgres_connection.execute(
                text(f"DROP DATABASE {database['database']} WITH (FORCE)")
            )
