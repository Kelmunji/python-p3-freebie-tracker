from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref, Session  # <-- add Session here
from sqlalchemy.ext.declarative import declarative_base

# ... rest of your code ...

# Use naming convention to help Alembic
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    freebies = relationship("Freebie", back_populates="company")

    def __repr__(self):
        return f"<Company {self.name}>"

    def devs(self):
        return list({freebie.dev for freebie in self.freebies})

    def give_freebie(self, dev, item_name, value):
        return Freebie(item_name=item_name, value=value, company=self, dev=dev)

    @classmethod
    def oldest_company(cls, session: Session):
        return session.query(cls).order_by(cls.founding_year.asc()).first()


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    freebies = relationship("Freebie", back_populates="dev")

    def __repr__(self):
        return f"<Dev {self.name}>"

    def companies(self):
        return list({freebie.company for freebie in self.freebies})

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev


class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)

    company_id = Column(Integer, ForeignKey('companies.id'))
    dev_id = Column(Integer, ForeignKey('devs.id'))

    company = relationship("Company", back_populates="freebies")
    dev = relationship("Dev", back_populates="freebies")

    def __repr__(self):
        return f"<Freebie {self.item_name} (${self.value})>"

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
