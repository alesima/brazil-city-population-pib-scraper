import pytest
from sqlalchemy import create_engine
from sqlalchemy import Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.models import Municipio

Base = declarative_base()


@pytest.fixture(scope="module")
def engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="module")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def session(engine, tables):
    Session = sessionmaker(bind=engine)
    return Session()


def test_municipio_table_structure():
    assert hasattr(Municipio, "id") and isinstance(
        Municipio.id.property.columns[0].type, Integer
    )
    assert hasattr(Municipio, "nome") and isinstance(
        Municipio.nome.property.columns[0].type, String
    )
    assert hasattr(Municipio, "estado") and isinstance(
        Municipio.estado.property.columns[0].type, String
    )
    assert hasattr(Municipio, "populacao") and isinstance(
        Municipio.populacao.property.columns[0].type, Integer
    )
    assert hasattr(Municipio, "pib_per_capita") and isinstance(
        Municipio.pib_per_capita.property.columns[0].type, Float
    )
    assert hasattr(Municipio, "possui_cicc") and isinstance(
        Municipio.possui_cicc.property.columns[0].type, Integer
    )
    assert hasattr(Municipio, "possui_gcm") and isinstance(
        Municipio.possui_gcm.property.columns[0].type, Integer
    )
    assert hasattr(Municipio, "possui_samu") and isinstance(
        Municipio.possui_samu.property.columns[0].type, Integer
    )


def test_municipio_table_defaults(session):
    municipio = Municipio(
        nome="TestCity", estado="TS", populacao=10000, pib_per_capita=50000.0
    )
    session.add(municipio)
    session.commit()

    fetched_municipio = session.query(Municipio).filter_by(nome="TestCity").first()
    assert fetched_municipio.possui_cicc == 0
    assert fetched_municipio.possui_gcm == 0
    assert fetched_municipio.possui_samu == 0


def test_municipio_insert_and_query(session):
    municipio = Municipio(
        nome="TestCity", estado="TS", populacao=10000, pib_per_capita=50000.0
    )
    session.add(municipio)
    session.commit()

    result = session.query(Municipio).filter_by(nome="TestCity").first()

    assert result is not None
    assert result.nome == "TestCity"
    assert result.estado == "TS"
    assert result.populacao == 10000
    assert result.pib_per_capita == 50000.0


def test_municipio_unique_id(session):
    municipio1 = Municipio(
        nome="CityOne", estado="A", populacao=1000, pib_per_capita=20000.0
    )
    municipio2 = Municipio(
        nome="CityTwo", estado="B", populacao=2000, pib_per_capita=30000.0
    )
    session.add_all([municipio1, municipio2])
    session.commit()

    assert municipio1.id != municipio2.id
