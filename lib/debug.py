from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie

engine = create_engine('sqlite:///freebie.db')
Session = sessionmaker(bind=engine)
session = Session()

# Fetch some test data
alice = session.query(Dev).filter_by(name="Alice").first()
google = session.query(Company).filter_by(name="Google").first()
first_freebie = session.query(Freebie).first()

print("\n--- Running automated debug tests ---\n")

# Test Dev.companies() method
print("Alice's companies:", alice.companies() if alice else "No Alice found")

# Test Dev.received_one() method
print("Has Alice received a 'T-shirt'? ->", alice.received_one("T-shirt") if alice else "No Alice found")

# Test Freebie.print_details()
if first_freebie:
    print("Freebie details:", first_freebie.print_details())
else:
    print("No freebies found")

# Test Company.oldest_company()
oldest = Company.oldest_company(session)
print("Oldest company:", oldest)

print("\n--- End of automated tests ---\n")

# Drop into ipdb to continue manual testing
import ipdb; ipdb.set_trace()
