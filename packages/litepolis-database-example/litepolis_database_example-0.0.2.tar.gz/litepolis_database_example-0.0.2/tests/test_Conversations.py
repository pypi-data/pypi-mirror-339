import pytest
# Import the DatabaseActor
from litepolis_database_example import DatabaseActor

# Note: Assumes a clean database state for each test or handles cleanup.

def test_create_conversation():
    """Tests creating a conversation via DatabaseActor."""
    title = "Test Create Conv"
    description = "Description for create test."
    creator_id = 1 # Assuming user ID 1 exists or is not enforced by FK here
    created_conv = None
    try:
        created_conv = DatabaseActor.create_conversation(
            title=title, description=description, creator_id=creator_id
        )
        assert created_conv is not None
        assert created_conv.id is not None
        assert created_conv.title == title
        assert created_conv.description == description
        assert created_conv.creator_id == creator_id
    finally:
        # Clean up
        if created_conv and created_conv.id:
            deleted = DatabaseActor.delete_conversation(created_conv.id)
            assert deleted is True

def test_read_conversation():
    """Tests reading a conversation via DatabaseActor."""
    title = "Test Read Conv"
    description = "Description for read test."
    creator_id = 2
    created_conv = None
    try:
        # Setup: Create a conversation
        created_conv = DatabaseActor.create_conversation(
            title=title, description=description, creator_id=creator_id
        )
        assert created_conv is not None
        assert created_conv.id is not None

        # Test: Read the conversation
        read_conv_obj = DatabaseActor.read_conversation(created_conv.id)
        assert read_conv_obj is not None
        assert read_conv_obj.id == created_conv.id
        assert read_conv_obj.title == title
        assert read_conv_obj.description == description
        assert read_conv_obj.creator_id == creator_id

        # Test: Read non-existent conversation
        non_existent_conv = DatabaseActor.read_conversation(99998)
        assert non_existent_conv is None
    finally:
        # Clean up
        if created_conv and created_conv.id:
            deleted = DatabaseActor.delete_conversation(created_conv.id)
            assert deleted is True

def test_read_conversations():
    """Tests reading multiple conversations via DatabaseActor."""
    initial_convs = DatabaseActor.read_conversations()
    initial_count = len(initial_convs)
    created_convs = []
    try:
        # Setup: Create conversations
        conv1 = DatabaseActor.create_conversation(title="Read All 1", description="Desc 1", creator_id=3)
        created_convs.append(conv1)
        conv2 = DatabaseActor.create_conversation(title="Read All 2", description="Desc 2", creator_id=4)
        created_convs.append(conv2)

        # Test: Read all conversations
        all_convs = DatabaseActor.read_conversations()
        assert isinstance(all_convs, list)
        assert len(all_convs) == initial_count + 2

        # Check if created conversations are in the list
        conv_ids_found = {c.id for c in all_convs}
        assert conv1.id in conv_ids_found
        assert conv2.id in conv_ids_found
    finally:
        # Clean up
        for conv in created_convs:
            if conv and conv.id:
                DatabaseActor.delete_conversation(conv.id)

def test_update_conversation():
    """Tests updating a conversation via DatabaseActor."""
    title = "Test Update Conv"
    description = "Original Description"
    creator_id = 5
    created_conv = None
    try:
        # Setup: Create a conversation
        created_conv = DatabaseActor.create_conversation(
            title=title, description=description, creator_id=creator_id
        )
        assert created_conv is not None
        assert created_conv.id is not None

        # Test: Update the description
        new_description = "Updated Description"
        updated_conv = DatabaseActor.update_conversation(
            conversation_id=created_conv.id,
            title=title, # Keep title same
            description=new_description,
            creator_id=creator_id # Keep creator same
        )
        assert updated_conv is not None
        assert updated_conv.id == created_conv.id
        assert updated_conv.description == new_description
        assert updated_conv.title == title # Ensure other fields didn't change

        # Verify by reading again
        read_again = DatabaseActor.read_conversation(created_conv.id)
        assert read_again is not None
        assert read_again.description == new_description

        # Test: Update non-existent conversation
        non_existent_update = DatabaseActor.update_conversation(99997, "No", "No Desc", 0)
        assert non_existent_update is None
    finally:
        # Clean up
        if created_conv and created_conv.id:
            deleted = DatabaseActor.delete_conversation(created_conv.id)
            assert deleted is True

def test_delete_conversation():
    """Tests deleting a conversation via DatabaseActor."""
    title = "Test Delete Conv"
    description = "Description for delete test."
    creator_id = 6
    created_conv = None
    try:
        # Setup: Create a conversation
        created_conv = DatabaseActor.create_conversation(
            title=title, description=description, creator_id=creator_id
        )
        assert created_conv is not None
        assert created_conv.id is not None
        conv_id = created_conv.id # Store ID

        # Test: Delete the conversation
        deleted = DatabaseActor.delete_conversation(conv_id)
        assert deleted is True

        # Verify: Try to read the deleted conversation
        read_deleted = DatabaseActor.read_conversation(conv_id)
        assert read_deleted is None

        # Test: Delete non-existent conversation
        deleted_non_existent = DatabaseActor.delete_conversation(99996)
        assert deleted_non_existent is False

        created_conv = None # Prevent cleanup attempt

    finally:
        # Clean up (should already be deleted)
        if created_conv and created_conv.id:
            DatabaseActor.delete_conversation(created_conv.id)
