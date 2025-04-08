from typing import List, Optional

from sqlmodel import Field, Session, SQLModel, select

# Import specific functions from utils
from .utils import get_session, create_db_and_tables

# Define the Comment model (remains the same)
class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    comment: str
    user_id: int
    conversation_id: int
    moderated: bool = False
    approved: bool = False
    # random: bool = False # Remove random, implement later if needed


# Introduce CommentManager class
class CommentManager:
    @staticmethod
    def create_comment(comment_text: str, user_id: int, conversation_id: int, moderated: bool = False, approved: bool = False) -> Comment:
        """Creates a new comment."""
        comment = Comment(
            comment=comment_text,
            user_id=user_id,
            conversation_id=conversation_id,
            moderated=moderated,
            approved=approved
        )
        session = get_session()
        session.add(comment)
        session.commit()
        session.refresh(comment)
        session.close()
        return comment

    @staticmethod
    def read_comment(comment_id: int) -> Optional[Comment]:
        """Reads a single comment by ID."""
        session = get_session()
        comment = session.get(Comment, comment_id)
        session.close()
        return comment

    @staticmethod
    def read_comments() -> List[Comment]:
        """Reads all comments."""
        session = get_session()
        comments = session.exec(select(Comment)).all()
        session.close()
        return comments

    @staticmethod
    def update_comment(comment_id: int, comment_text: str, moderated: bool, approved: bool) -> Optional[Comment]:
        """Updates an existing comment's text, moderated, and approved status."""
        # Note: user_id and conversation_id are typically not updated.
        session = get_session()
        db_comment = session.get(Comment, comment_id)
        if not db_comment:
            session.close()
            return None # Comment not found

        # Update fields
        db_comment.comment = comment_text
        db_comment.moderated = moderated
        db_comment.approved = approved

        session.add(db_comment)
        session.commit()
        session.refresh(db_comment)
        session.close()
        return db_comment

    @staticmethod
    def delete_comment(comment_id: int) -> bool:
        """Deletes a comment by ID."""
        session = get_session()
        comment = session.get(Comment, comment_id)
        if not comment:
            session.close()
            return False # Comment not found

        session.delete(comment)
        session.commit()
        session.close()
        return True

# Run this once to create the database and tables (remains the same)
create_db_and_tables()
