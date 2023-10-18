from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from schemas import UserType

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String, nullable=False)
    user_type = Column(String, nullable=False)
    address = Column(Text, nullable=False)
    motivation = Column(Text, nullable=False)

    @validates('name', 'city', 'country', 'address')
    def validate_string_fields(self, key, value):
        assert isinstance(value, str), f"{key.capitalize()} must be a string"
        stripped_value = value.strip()
        assert stripped_value, f"{key.capitalize()} cannot be null or empty"
        return stripped_value

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, "Invalid email address"
        return email

    @validates('phone')
    def validate_phone(self, key, phone):
        assert phone.isdigit() and len(phone) == 11, "Invalid phone number"
        return phone

    @validates('age')
    def validate_age(self, key, age):
        assert age > 0, "Age must be a positive integer"
        return age

    @validates('user_type')
    def validate_user_type(self, key, value):
        assert value in [item.value for item in UserType], "Invalid user type"
        return value

    def __repr__(self):
        return f"""
            User(
                id={self.id},
                name={self.name},
                email={self.email},
                city={self.city},
                country={self.country},
                age={self.age},
                phone={self.phone},
                address={self.address},
                motivation={self.motivation}
            )
        """
