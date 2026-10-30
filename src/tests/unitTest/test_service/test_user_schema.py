import pytest
from pydantic import ValidationError

from src.schema.userSchema import UserRequest

def test_user_schema_accept_valid_input():
    user = UserRequest(
        email="test@example.com",
        password="example-password"
    )
    assert user.email == "test@example.com"

def test_user_schema_reject_invalid_email():
    with pytest.raises(ValidationError):
        UserRequest(
            email="not-an-email",
            password="not-a-password"
        )