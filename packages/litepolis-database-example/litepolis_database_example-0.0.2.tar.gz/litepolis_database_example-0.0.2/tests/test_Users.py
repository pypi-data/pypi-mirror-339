import pytest
# Import the DatabaseActor from the refactored package
from litepolis_database_example import DatabaseActor

# Note: Assumes a clean database state for each test or handles cleanup.
# Using pytest fixtures for setup/teardown would be more robust.

def test_create_user():
    """Tests creating a user via DatabaseActor."""
    email = "create@example.com"
    password = "password"
    privilege = "user"
    created_user = None # Initialize
    try:
        created_user = DatabaseActor.create_user(email=email, password=password, privilege=privilege)
        assert created_user is not None
        assert created_user.id is not None
        assert created_user.email == email
        assert created_user.password == password # In real app, password should be hashed
        assert created_user.privilege == privilege
    finally:
        # Clean up
        if created_user and created_user.id:
            deleted = DatabaseActor.delete_user(created_user.id)
            assert deleted is True

def test_read_user():
    """Tests reading a user via DatabaseActor."""
    email = "read@example.com"
    password = "password"
    privilege = "tester"
    created_user = None
    try:
        # Setup: Create a user first
        created_user = DatabaseActor.create_user(email=email, password=password, privilege=privilege)
        assert created_user is not None
        assert created_user.id is not None

        # Test: Read the user
        read_user_obj = DatabaseActor.read_user(created_user.id)
        assert read_user_obj is not None
        assert read_user_obj.id == created_user.id
        assert read_user_obj.email == email
        assert read_user_obj.privilege == privilege

        # Test: Read non-existent user
        non_existent_user = DatabaseActor.read_user(99999) # Assuming 99999 doesn't exist
        assert non_existent_user is None
    finally:
        # Clean up
        if created_user and created_user.id:
            deleted = DatabaseActor.delete_user(created_user.id)
            assert deleted is True

def test_read_users():
    """Tests reading multiple users via DatabaseActor."""
    initial_users = DatabaseActor.read_users()
    initial_count = len(initial_users)
    created_users = []
    try:
        # Setup: Create a couple of users
        user1 = DatabaseActor.create_user(email="read1@example.com", password="pw1", privilege="u1")
        created_users.append(user1)
        user2 = DatabaseActor.create_user(email="read2@example.com", password="pw2", privilege="u2")
        created_users.append(user2)

        # Test: Read all users
        all_users = DatabaseActor.read_users()
        assert isinstance(all_users, list)
        assert len(all_users) == initial_count + 2

        # Check if created users are in the list (order might vary)
        user_ids_found = {u.id for u in all_users}
        assert user1.id in user_ids_found
        assert user2.id in user_ids_found

    finally:
        # Clean up
        for user in created_users:
            if user and user.id:
                DatabaseActor.delete_user(user.id)

def test_update_user():
    """Tests updating a user via DatabaseActor."""
    email = "update@example.com"
    password = "old_password"
    privilege = "user"
    created_user = None
    try:
        # Setup: Create a user
        created_user = DatabaseActor.create_user(email=email, password=password, privilege=privilege)
        assert created_user is not None
        assert created_user.id is not None

        # Test: Update the user's privilege
        new_privilege = "admin"
        updated_user = DatabaseActor.update_user(
            user_id=created_user.id,
            email=email, # Keep email same
            password=password, # Keep password same
            privilege=new_privilege
        )
        assert updated_user is not None
        assert updated_user.id == created_user.id
        assert updated_user.privilege == new_privilege
        assert updated_user.email == email # Ensure other fields didn't change unexpectedly

        # Verify by reading again
        read_again = DatabaseActor.read_user(created_user.id)
        assert read_again is not None
        assert read_again.privilege == new_privilege

        # Test: Update non-existent user
        non_existent_update = DatabaseActor.update_user(99999, "no@no.com", "nopw", "no")
        assert non_existent_update is None

    finally:
        # Clean up
        if created_user and created_user.id:
            deleted = DatabaseActor.delete_user(created_user.id)
            assert deleted is True

def test_delete_user():
    """Tests deleting a user via DatabaseActor."""
    email = "delete@example.com"
    password = "password"
    privilege = "temp"
    created_user = None
    try:
        # Setup: Create a user
        created_user = DatabaseActor.create_user(email=email, password=password, privilege=privilege)
        assert created_user is not None
        assert created_user.id is not None
        user_id = created_user.id # Store ID for later checks

        # Test: Delete the user
        deleted = DatabaseActor.delete_user(user_id)
        assert deleted is True

        # Verify: Try to read the deleted user
        read_deleted = DatabaseActor.read_user(user_id)
        assert read_deleted is None

        # Test: Delete non-existent user
        deleted_non_existent = DatabaseActor.delete_user(99999)
        assert deleted_non_existent is False

        created_user = None # Prevent cleanup attempt in finally block

    finally:
        # Clean up (should already be deleted in the test)
        if created_user and created_user.id:
            DatabaseActor.delete_user(created_user.id) # Attempt cleanup just in case test failed before delete assertion
