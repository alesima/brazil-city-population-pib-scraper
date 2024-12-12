from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Base, Municipio


class DatabaseManager:
    def __init__(self, db_url='sqlite:///municipios.db'):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_city(self, city: Municipio):
        existing_city = self.session.query(Municipio).filter_by(
            id=city.id).first()

        if existing_city:
            return

        self.session.add(city)
        self.session.commit()

    def get_all_cities(self):
        return self.session.query(Municipio).all()

    def close(self):
        self.session.close()
