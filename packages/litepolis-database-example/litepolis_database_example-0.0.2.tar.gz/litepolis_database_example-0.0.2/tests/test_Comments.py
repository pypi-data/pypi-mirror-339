import pytest
from litepolis_database_example import DatabaseActor

# Note: Assumes a clean database state for each test or handles cleanup.
# Assumes user_id=1 and conversation_id=1 exist or FKs are not enforced.

def test_create_comment():
    """Tests creating a comment via DatabaseActor."""
    comment_text = "Test create comment text."
    user_id = 1
    conversation_id = 1
    created_comment = None
    try:
        created_comment = DatabaseActor.create_comment(
            comment_text=comment_text, user_id=user_id, conversation_id=conversation_id
        )
        assert created_comment is not None
        assert created_comment.id is not None
        assert created_comment.comment == comment_text
        assert created_comment.user_id == user_id
        assert created_comment.conversation_id == conversation_id
        assert created_comment.moderated is False # Default value check
        assert created_comment.approved is False # Default value check
    finally:
        # Clean up
        if created_comment and created_comment.id:
            deleted = DatabaseActor.delete_comment(created_comment.id)
            assert deleted is True

def test_read_comment():
    """Tests reading a comment via DatabaseActor."""
    comment_text = "Test read comment text."
    user_id = 2
    conversation_id = 2
    created_comment = None
    try:
        # Setup: Create a comment
        created_comment = DatabaseActor.create_comment(
            comment_text=comment_text, user_id=user_id, conversation_id=conversation_id
        )
        assert created_comment is not None
        assert created_comment.id is not None

        # Test: Read the comment
        read_comment_obj = DatabaseActor.read_comment(created_comment.id)
        assert read_comment_obj is not None
        assert read_comment_obj.id == created_comment.id
        assert read_comment_obj.comment == comment_text
        assert read_comment_obj.user_id == user_id
        assert read_comment_obj.conversation_id == conversation_id

        # Test: Read non-existent comment
        non_existent_comment = DatabaseActor.read_comment(99995)
        assert non_existent_comment is None
    finally:
        # Clean up
        if created_comment and created_comment.id:
            deleted = DatabaseActor.delete_comment(created_comment.id)
            assert deleted is True

def test_read_comments():
    """Tests reading multiple comments via DatabaseActor."""
    initial_comments = DatabaseActor.read_comments()
    initial_count = len(initial_comments)
    created_comments = []
    try:
        # Setup: Create comments
        comment1 = DatabaseActor.create_comment(comment_text="Read All C1", user_id=3, conversation_id=3)
        created_comments.append(comment1)
        comment2 = DatabaseActor.create_comment(comment_text="Read All C2", user_id=4, conversation_id=4)
        created_comments.append(comment2)

        # Test: Read all comments
        all_comments = DatabaseActor.read_comments()
        assert isinstance(all_comments, list)
        assert len(all_comments) == initial_count + 2

        # Check if created comments are in the list
        comment_ids_found = {c.id for c in all_comments}
        assert comment1.id in comment_ids_found
        assert comment2.id in comment_ids_found
    finally:
        # Clean up
        for comment in created_comments:
            if comment and comment.id:
                DatabaseActor.delete_comment(comment.id)

def test_update_comment():
    """Tests updating a comment via DatabaseActor."""
    comment_text = "Original comment text"
    user_id = 5
    conversation_id = 5
    created_comment = None
    try:
        # Setup: Create a comment
        created_comment = DatabaseActor.create_comment(
            comment_text=comment_text, user_id=user_id, conversation_id=conversation_id
        )
        assert created_comment is not None
        assert created_comment.id is not None
        assert created_comment.moderated is False
        assert created_comment.approved is False

        # Test: Update the comment text and flags
        new_text = "Updated comment text"
        new_moderated = True
        new_approved = True
        updated_comment = DatabaseActor.update_comment(
            comment_id=created_comment.id,
            comment_text=new_text,
            moderated=new_moderated,
            approved=new_approved
        )
        assert updated_comment is not None
        assert updated_comment.id == created_comment.id
        assert updated_comment.comment == new_text
        assert updated_comment.moderated == new_moderated
        assert updated_comment.approved == new_approved
        assert updated_comment.user_id == user_id # Ensure other fields didn't change

        # Verify by reading again
        read_again = DatabaseActor.read_comment(created_comment.id)
        assert read_again is not None
        assert read_again.comment == new_text
        assert read_again.moderated == new_moderated
        assert read_again.approved == new_approved

        # Test: Update non-existent comment
        non_existent_update = DatabaseActor.update_comment(99994, "No Text", False, False)
        assert non_existent_update is None
    finally:
        # Clean up
        if created_comment and created_comment.id:
            deleted = DatabaseActor.delete_comment(created_comment.id)
            assert deleted is True

def test_delete_comment():
    """Tests deleting a comment via DatabaseActor."""
    comment_text = "Test delete comment text."
    user_id = 6
    conversation_id = 6
    created_comment = None
    try:
        # Setup: Create a comment
        created_comment = DatabaseActor.create_comment(
            comment_text=comment_text, user_id=user_id, conversation_id=conversation_id
        )
        assert created_comment is not None
        assert created_comment.id is not None
        comment_id = created_comment.id # Store ID

        # Test: Delete the comment
        deleted = DatabaseActor.delete_comment(comment_id)
        assert deleted is True

        # Verify: Try to read the deleted comment
        read_deleted = DatabaseActor.read_comment(comment_id)
        assert read_deleted is None

        # Test: Delete non-existent comment
        deleted_non_existent = DatabaseActor.delete_comment(99993)
        assert deleted_non_existent is False

        created_comment = None # Prevent cleanup attempt

    finally:
        # Clean up (should already be deleted)
        if created_comment and created_comment.id:
            DatabaseActor.delete_comment(created_comment.id)
