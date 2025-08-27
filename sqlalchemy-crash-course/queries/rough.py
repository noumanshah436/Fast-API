from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.user import User, Role
from main import session

from sqlalchemy import text

# Raw SQL with text()
query = text("SELECT first_name, last_name FROM users WHERE first_name = :name")
raw_results = session.execute(query, {"name": "John"}).all()
print(f"Raw SQL results: {raw_results}")

# Text with parameters
query = text("SELECT COUNT(*) as count FROM users WHERE first_name LIKE :pattern")
count_result = session.execute(query, {"pattern": "J%"}).scalar()
print(f"Raw SQL count: {count_result}")