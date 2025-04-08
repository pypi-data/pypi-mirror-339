import pytest
# Import the necessary components directly
from litepolis_database_example import DatabaseActor, Conversation

# Note: These tests assume a clean database state before each run or handle cleanup.
# Using pytest fixtures would be more robust for managing state.
# Also assumes the underlying DB (database.db or database-test.db if utils was modified) exists.

# --- User Tests ---

def test_actor_create_user():
    """Tests creating a user via DatabaseActor."""
    email = "actor_create@example.com"
    password = "password"
    privilege = "user"
    created_user = None
    try:
        created_user = DatabaseActor.create_user(email=email, password=password, privilege=privilege)
        assert created_user is not None
        assert created_user.id is not None
        assert created_user.email == email
    finally:
        if created_user and created_user.id:
            deleted = DatabaseActor.delete_user(created_user.id)
            assert deleted is True

def test_actor_read_user():
    """Tests reading a user via DatabaseActor."""
    email = "actor_read@example.com"
    password = "password"
    created_user = None
    try:
        created_user = DatabaseActor.create_user(email=email, password=password)
        assert created_user and created_user.id
        fetched_user = DatabaseActor.read_user(created_user.id)
        assert fetched_user is not None
        assert fetched_user.email == email
        assert fetched_user.id == created_user.id
    finally:
        if created_user and created_user.id:
            deleted = DatabaseActor.delete_user(created_user.id)
            assert deleted is True

def test_actor_read_users():
    """Tests reading all users via DatabaseActor."""
    # Simple check that it returns a list
    users = DatabaseActor.read_users()
    assert isinstance(users, list)

def test_actor_update_user():
    """Tests updating a user via DatabaseActor."""
    email = "actor_update@example.com"
    password = "old_password"
    privilege = "user"
    created_user = None
    try:
        created_user = DatabaseActor.create_user(email=email, password=password, privilege=privilege)
        assert created_user and created_user.id

        updated_user = DatabaseActor.update_user(
            user_id=created_user.id,
            email="actor_update_new@example.com", # Update email
            password="new_password",             # Update password
            privilege="admin"                    # Update privilege
        )
        assert updated_user is not None
        assert updated_user.id == created_user.id
        assert updated_user.email == "actor_update_new@example.com"
        assert updated_user.privilege == "admin"
        # Password check is tricky without hashing/retrieval logic
    finally:
        if created_user and created_user.id:
            deleted = DatabaseActor.delete_user(created_user.id)
            assert deleted is True

def test_actor_delete_user():
    """Tests deleting a user via DatabaseActor."""
    email = "actor_delete@example.com"
    password = "password"
    created_user = None
    try:
        created_user = DatabaseActor.create_user(email=email, password=password)
        assert created_user and created_user.id
        user_id = created_user.id

        deleted = DatabaseActor.delete_user(user_id)
        assert deleted is True

        # Verify deletion
        fetched_user = DatabaseActor.read_user(user_id)
        assert fetched_user is None
        created_user = None # Prevent double delete in finally
    finally:
        if created_user and created_user.id:
            DatabaseActor.delete_user(created_user.id)


# --- Conversation Tests ---

def test_actor_create_conversation():
    """Tests creating a conversation via DatabaseActor."""
    title = "Actor Conv Title"
    description = "Actor Conv Desc"
    creator_user = None
    created_conv = None
    try:
        # Need a user first (assuming FKs might be enforced)
        creator_user = DatabaseActor.create_user(email="actor_conv_creator@example.com", password="pw")
        assert creator_user and creator_user.id

        created_conv = DatabaseActor.create_conversation(
            title=title, description=description, creator_id=creator_user.id
        )
        assert created_conv is not None
        assert created_conv.id is not None
        assert created_conv.title == title
        assert created_conv.creator_id == creator_user.id
    finally:
        if created_conv and created_conv.id:
            deleted_conv = DatabaseActor.delete_conversation(created_conv.id)
            assert deleted_conv is True
        if creator_user and creator_user.id:
            deleted_user = DatabaseActor.delete_user(creator_user.id)
            assert deleted_user is True

def test_actor_read_conversation():
    """Tests reading a conversation via DatabaseActor."""
    title = "Actor Read Conv"
    creator_user = None
    created_conv = None
    try:
        creator_user = DatabaseActor.create_user(email="actor_conv_reader@example.com", password="pw")
        assert creator_user and creator_user.id
        created_conv = DatabaseActor.create_conversation(title=title, description="Read Desc", creator_id=creator_user.id)
        assert created_conv and created_conv.id

        fetched_conv = DatabaseActor.read_conversation(created_conv.id)
        assert fetched_conv is not None
        assert fetched_conv.id == created_conv.id
        assert fetched_conv.title == title
    finally:
        if created_conv and created_conv.id:
            deleted_conv = DatabaseActor.delete_conversation(created_conv.id)
            assert deleted_conv is True
        if creator_user and creator_user.id:
            deleted_user = DatabaseActor.delete_user(creator_user.id)
            assert deleted_user is True

# --- Comment Tests ---

def test_actor_create_comment():
    """Tests creating a comment via DatabaseActor."""
    comment_text = "Actor comment text"
    creator_user = None
    created_conv = None
    created_comment = None
    try:
        creator_user = DatabaseActor.create_user(email="actor_comment_creator@example.com", password="pw")
        assert creator_user and creator_user.id
        created_conv = DatabaseActor.create_conversation(title="Conv for Comment", description="Desc", creator_id=creator_user.id)
        assert created_conv and created_conv.id

        created_comment = DatabaseActor.create_comment(
            comment_text=comment_text, user_id=creator_user.id, conversation_id=created_conv.id
        )
        assert created_comment is not None
        assert created_comment.id is not None
        assert created_comment.comment == comment_text
        assert created_comment.user_id == creator_user.id
        assert created_comment.conversation_id == created_conv.id
    finally:
        if created_comment and created_comment.id:
            deleted_comment = DatabaseActor.delete_comment(created_comment.id)
            assert deleted_comment is True
        if created_conv and created_conv.id:
            deleted_conv = DatabaseActor.delete_conversation(created_conv.id)
            assert deleted_conv is True
        if creator_user and creator_user.id:
            deleted_user = DatabaseActor.delete_user(creator_user.id)
            assert deleted_user is True

def test_actor_update_comment():
    """Tests updating a comment via DatabaseActor."""
    creator_user = None
    created_conv = None
    created_comment = None
    try:
        creator_user = DatabaseActor.create_user(email="actor_comment_updater@example.com", password="pw")
        assert creator_user and creator_user.id
        created_conv = DatabaseActor.create_conversation(title="Conv for Update Comment", description="Desc", creator_id=creator_user.id)
        assert created_conv and created_conv.id
        created_comment = DatabaseActor.create_comment(comment_text="Original", user_id=creator_user.id, conversation_id=created_conv.id)
        assert created_comment and created_comment.id

        updated_comment = DatabaseActor.update_comment(
            comment_id=created_comment.id,
            comment_text="Updated Text",
            moderated=True,
            approved=False
        )
        assert updated_comment is not None
        assert updated_comment.id == created_comment.id
        assert updated_comment.comment == "Updated Text"
        assert updated_comment.moderated is True
        assert updated_comment.approved is False
    finally:
        # Cleanup order matters if FKs are enforced
        if created_comment and created_comment.id:
            deleted_comment = DatabaseActor.delete_comment(created_comment.id)
            assert deleted_comment is True
        if created_conv and created_conv.id:
            deleted_conv = DatabaseActor.delete_conversation(created_conv.id)
            assert deleted_conv is True
        if creator_user and creator_user.id:
            deleted_user = DatabaseActor.delete_user(creator_user.id)
            assert deleted_user is True

# Add more tests as needed for read_comments, update_conversation, delete_conversation, etc. via Actor
