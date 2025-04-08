from typing import List, Optional

from sqlmodel import Field, Session, SQLModel, select

# Import specific functions from utils
from .utils import get_session, create_db_and_tables

# Define the Conversation model (remains the same)
class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    creator_id: int
    # moderation: bool = False # Add moderation if needed


# Introduce ConversationManager class
class ConversationManager:
    @staticmethod
    def create_conversation(title: str, description: str, creator_id: int) -> Conversation:
        """Creates a new conversation."""
        conversation = Conversation(title=title, description=description, creator_id=creator_id)
        session = get_session()
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        session.close()
        return conversation

    @staticmethod
    def read_conversation(conversation_id: int) -> Optional[Conversation]:
        """Reads a single conversation by ID."""
        session = get_session()
        conversation = session.get(Conversation, conversation_id)
        session.close()
        return conversation

    @staticmethod
    def read_conversations() -> List[Conversation]:
        """Reads all conversations."""
        session = get_session()
        conversations = session.exec(select(Conversation)).all()
        session.close()
        return conversations

    @staticmethod
    def update_conversation(conversation_id: int, title: str, description: str, creator_id: int) -> Optional[Conversation]:
        """Updates an existing conversation."""
        session = get_session()
        db_conversation = session.get(Conversation, conversation_id)
        if not db_conversation:
            session.close()
            return None # Conversation not found

        # Update fields
        db_conversation.title = title
        db_conversation.description = description
        db_conversation.creator_id = creator_id # Assuming creator_id can be updated

        session.add(db_conversation)
        session.commit()
        session.refresh(db_conversation)
        session.close()
        return db_conversation

    @staticmethod
    def delete_conversation(conversation_id: int) -> bool:
        """Deletes a conversation by ID."""
        session = get_session()
        conversation = session.get(Conversation, conversation_id)
        if not conversation:
            session.close()
            return False # Conversation not found

        session.delete(conversation)
        session.commit()
        session.close()
        return True

# Run this once to create the database and tables (remains the same)
create_db_and_tables()
