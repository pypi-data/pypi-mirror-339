import os
from sqlmodel import Session, SQLModel, create_engine
from litepolis import get_config

DEFAULT_CONFIG = {
    "sqlite_url": "sqlite:///database.db"
}

# Use .get() for safer access and prepare for potential external config
# In a real scenario, you might integrate litepolis.get_config here
database_url = DEFAULT_CONFIG.get("sqlite_url")

# Handle potential test environment override (optional but good practice)
if ("PYTEST_CURRENT_TEST" not in os.environ and
    "PYTEST_VERSION" not in os.environ):
    database_url = get_config("litepolis_database_example", "sqlite_url")

engine = create_engine(database_url)

# connect_db seems redundant if engine is created at module level,
# but keeping it for consistency with template for now.
def connect_db():
    global engine
    # Re-create engine based on potentially updated config if needed
    db_url = DEFAULT_CONFIG.get("sqlite_url") # Or get_config
    engine = create_engine(db_url)

def create_db_and_tables():
    # SQLModel.metadata.create_all() has checkfirst=True by default
    SQLModel.metadata.create_all(engine)

# Keep get_session for now, might be removed later if completely unused
def get_session():
    return Session(engine)