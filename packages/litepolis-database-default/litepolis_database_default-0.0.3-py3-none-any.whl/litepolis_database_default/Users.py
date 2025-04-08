"""
This module defines the User model and UserManager class for interacting with the 'users' table in the database.

The 'users' table stores information about users, including their email, authentication token, and admin status.
It also includes timestamps for creation and modification.

.. list-table:: Table Schema
   :header-rows: 1

   * - Column
     - Type
     - Description
   * - id
     - INTEGER
     - Unique identifier for the user.
   * - email
     - VARCHAR
     - User's email address. Must be unique.
   * - auth_token
     - VARCHAR
     - Authentication token for the user.
   * - is_admin
     - BOOLEAN
     - Indicates whether the user is an administrator.
   * - created
     - DATETIME
     - Timestamp indicating when the user was created.
   * - modified
     - DATETIME
     - Timestamp indicating when the user was last modified.

.. list-table:: Relationships

    * - Report
      - One-to-many.
    * - Comment
      - One-to-many.
    * - Vote
      - One-to-many.

The UserManager class provides static methods for performing CRUD (Create, Read, Update, Delete) operations
on the 'users' table.

To use the methods in this module, import DatabaseActor.  For example::

    from litepolis_database_default import DatabaseActor

    user = DatabaseActor.create_user({
        "email": "test@example.com",
        "auth_token": "auth_token",
    })
"""

from sqlmodel import SQLModel, Field, Relationship, Column
from sqlmodel import Index, UniqueConstraint, Session, select
from typing import Optional, List, Type, Any, Dict, Generator
from datetime import datetime, UTC

from .utils import get_session 

class BaseModel(SQLModel):
    id: int = Field(primary_key=True)
    created: datetime = Field(default_factory=lambda: datetime.now(UTC))
    modified: datetime = Field(default_factory=lambda: datetime.now(UTC))

class User(BaseModel, table=True):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
        Index("ix_user_created", "created"),
        Index("ix_user_is_admin", "is_admin"),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, unique=True)
    auth_token: str = Field(nullable=False)
    is_admin: bool = Field(default=False)
    created: datetime = Field(default_factory=lambda: datetime.now(UTC))
    modified: datetime = Field(default_factory=lambda: datetime.now(UTC))

    reports: List["Report"] = Relationship(back_populates="reporter")
    comments: List["Comment"] = Relationship(back_populates="user")
    votes: List["Vote"] = Relationship(back_populates="user")

class UserManager:
    @staticmethod
    def create_user(data: Dict[str, Any]) -> User:
        """Creates a new User record.

        To use this method, import DatabaseActor.  For example::

            from litepolis_database_default import DatabaseActor

            user = DatabaseActor.create_user({
                "email": "test@example.com",
                "auth_token": "auth_token",
            })
        """
        with get_session() as session:
            user_instance = User(**data)
            session.add(user_instance)
            session.commit()
            session.refresh(user_instance)
            return user_instance

    @staticmethod
    def read_user(user_id: int) -> Optional[User]:
        """Reads a User record by ID.

        To use this method, import DatabaseActor.  For example::

            from litepolis_database_default import DatabaseActor

            user = DatabaseActor.read_user(user_id=1)
        """
        with get_session() as session:
            return session.get(User, user_id)

    @staticmethod
    def read_user_by_email(email: str) -> Optional[User]:
        """Reads a User record by email.

        To use this method, import DatabaseActor.  For example::

            from litepolis_database_default import DatabaseActor

            user = DatabaseActor.read_user_by_email(email="test@example.com")
        """
        with get_session() as session:
            return session.exec(select(User).where(User.email == email)).first()


    @staticmethod
    def list_users(page: int = 1, page_size: int = 10) -> List[User]:
        """Lists User records with pagination.

        To use this method, import DatabaseActor.  For example::

            from litepolis_database_default import DatabaseActor

            users = DatabaseActor.list_users(page=1, page_size=10)
        """
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10
        offset = (page - 1) * page_size
        with get_session() as session:
            return session.exec(select(User).offset(offset).limit(page_size)).all()


    @staticmethod
    def update_user(user_id: int, data: Dict[str, Any]) -> Optional[User]:
        """Updates a User record by ID.

        To use this method, import DatabaseActor.  For example::

            from litepolis_database_default import DatabaseActor

            user = DatabaseActor.update_user(user_id=1, data={"email": "new_email@example.com"})
        """
        with get_session() as session:
            user_instance = session.get(User, user_id)
            if not user_instance:
                return None
            for key, value in data.items():
                setattr(user_instance, key, value)
            session.add(user_instance)
            session.commit()
            session.refresh(user_instance)
            return user_instance

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """Deletes a User record by ID. Returns True if successful.

        To use this method, import DatabaseActor.  For example::

            from litepolis_database_default import DatabaseActor

            success = DatabaseActor.delete_user(user_id=1)
        """
        with get_session() as session:
            user_instance = session.get(User, user_id)
            if not user_instance:
                return False
            session.delete(user_instance)
            session.commit()
            return True
            
    @staticmethod
    def search_users_by_email(query: str) -> List[User]:
        """Search users by email.

        To use this method, import DatabaseActor.  For example::

            from litepolis_database_default import DatabaseActor

            users = DatabaseActor.search_users_by_email(query="example.com")
        """
        with get_session() as session:
            return session.exec(select(User).where(User.email.contains(query))).all()

    @staticmethod
    def list_users_by_admin_status(is_admin: bool) -> List[User]:
        """List users by admin status.

        To use this method, import DatabaseActor.  For example::

            from litepolis_database_default import DatabaseActor

            users = DatabaseActor.list_users_by_admin_status(is_admin=True)
        """
        with get_session() as session:
            return session.exec(select(User).where(User.is_admin == is_admin)).all()

    @staticmethod
    def list_users_created_in_date_range(start_date: datetime, end_date: datetime) -> List[User]:
        """List users created in a date range.

        To use this method, import DatabaseActor.  For example::

            from litepolis_database_default import DatabaseActor

            users = DatabaseActor.list_users_created_in_date_range(start_date=datetime(2023, 1, 1), end_date=datetime(2023, 12, 31))
        """
        with get_session() as session:
            return session.exec(
                select(User).where(User.created >= start_date, User.created <= end_date)
            ).all()

    @staticmethod
    def count_users() -> int:
        """Counts all User records.

        To use this method, import DatabaseActor.  For example:

            from litepolis_database_default import DatabaseActor

            count = DatabaseActor.count_users()
        """
        with get_session() as session:
            return session.scalar(select(User).count()) or 0