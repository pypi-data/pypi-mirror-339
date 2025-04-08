from typing import Optional, List

from sqlmodel import Field, Session, SQLModel, select

# Import specific functions from utils
from .utils import get_session, create_db_and_tables

# Define the SQLModel for users (remains the same)
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password: str
    privilege: str = "user"


# Introduce UserManager class based on the template
class UserManager:
    @staticmethod
    def create_user(email: str, password: str, privilege: str = "user") -> User:
        """Creates a new user in the database."""
        user = User(email=email, password=password, privilege=privilege)
        session = get_session()
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()
        return user # Return the created user object

    @staticmethod
    def read_user(user_id: int) -> Optional[User]:
        """Reads a single user by ID."""
        user = None # Initialize user to None
        session = get_session()
        user = session.get(User, user_id)
        session.close()
        return user # Returns the user or None if not found

    @staticmethod
    def read_users() -> List[User]:
        """Reads all users from the database."""
        users = [] # Initialize users list
        session = get_session()
        users = session.exec(select(User)).all()
        session.close()
        return users

    @staticmethod
    def update_user(user_id: int, email: str, password: str, privilege: str) -> Optional[User]:
        """Updates an existing user's details."""
        db_user = None # Initialize db_user
        session = get_session()
        db_user = session.get(User, user_id)
        if not db_user:
            session.close()
            return None # User not found

        # Update fields directly
        db_user.email = email
        db_user.password = password
        db_user.privilege = privilege

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        session.close()
        return db_user # Return the updated user or None if not found initially

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """Deletes a user by ID."""
        deleted = False # Flag to track deletion
        session = get_session()
        user = session.get(User, user_id)
        if not user:
            session.close()
            return False # User not found

        session.delete(user)
        session.commit()
        session.close()
        deleted = True
        return deleted # Return True if deleted, False otherwise

# Run this once to create the database and tables (remains the same)
create_db_and_tables()
