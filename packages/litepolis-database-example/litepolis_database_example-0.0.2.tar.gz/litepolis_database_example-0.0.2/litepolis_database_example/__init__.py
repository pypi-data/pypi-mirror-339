# Import configuration and utility functions/classes
from .utils import DEFAULT_CONFIG

# Import the main interaction point
from .Actor import DatabaseActor

# Import the data models
from .Users import User
from .Conversations import Conversation
from .Comments import Comment

# Optionally, run table creation on import if desired,
# though it's already called within each model file.
# Consider removing it from model files if called here centrally.
# create_db_and_tables()

# Define what gets imported when using 'from package import *'
__all__ = [
    "DEFAULT_CONFIG",
    "DatabaseActor",
    "User",
    "Conversation",
    "Comment"
]