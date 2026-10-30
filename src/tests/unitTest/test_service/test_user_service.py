from unittest.mock import AsyncMock
import pytest
from src.service.userService import UserService

@pytest.mark.asyncio
async def test_get_user_returns_repository_result():
    repository = AsyncMock()

    expected_user = {"id":1,"email":"test@example.com","token":"9fj*$&hfj94ihf84*#jf490JHF80-484uiO*$hfF94)"}
    repository.getUser.return_value = expected_user

    service  = UserService(repository)

    result = await service.getUser("amir@gmail.com")

    assert result == expected_user
    repository.getUser.assert_awaited_once_with("amir@gmail.com")
