from typing import Dict, Any, List

# Import the manager classes from the refactored files
from .Users import UserManager
from .Conversations import ConversationManager
from .Comments import CommentManager

# Define DatabaseActor inheriting from all managers
class DatabaseActor(UserManager, ConversationManager, CommentManager):
    """
    Aggregates database management functionalities for Users, Conversations, and Comments.
    Inherits all static methods from the respective manager classes.
    """
    pass # No additional methods needed as it inherits everything