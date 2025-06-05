from models import Base, Company, Dev, Freebie
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///freebie.db')
Session = sessionmaker(bind=engine)
session = Session()

# Drop and recreate tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Create Companies
c1 = Company(name="Google", founding_year=1998)
c2 = Company(name="Apple", founding_year=1976)

# Create Devs
d1 = Dev(name="Alice")
d2 = Dev(name="Bob")

# Create Freebies
f1 = Freebie(item_name="Sticker", value=5, company=c1, dev=d1)
f2 = Freebie(item_name="T-shirt", value=20, company=c2, dev=d1)
f3 = Freebie(item_name="Mug", value=15, company=c1, dev=d2)

# Add all to session
session.add_all([c1, c2, d1, d2, f1, f2, f3])
session.commit()
