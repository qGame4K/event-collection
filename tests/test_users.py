import pytest

from users import add_user, find_users, is_email_taken, sort_users


def test_add_user():
    users = []
    user = add_user(users, "Иван", "ivan@example.com")
    assert user == {"id": 1, "name": "Иван", "email": "ivan@example.com"}
    assert len(users) == 1


def test_is_email_taken():
    users = [{"id": 1, "name": "Иван", "email": "ivan@example.com"}]
    assert is_email_taken(users, "IVAN@example.com")
    assert not is_email_taken(users, "anna@example.com")


def test_add_user_with_taken_email():
    users = []
    add_user(users, "Иван", "ivan@example.com")
    with pytest.raises(ValueError):
        add_user(users, "Иван Петров", "ivan@example.com")


def test_find_users():
    users = []
    add_user(users, "Иван", "ivan@example.com")
    add_user(users, "Анна", "anna@example.com")
    assert find_users(users, "анн") == [users[1]]


def test_sort_users():
    users = []
    add_user(users, "Иван", "ivan@example.com")
    add_user(users, "Анна", "anna@example.com")
    names = [user["name"] for user in sort_users(users)]
    assert names == ["Анна", "Иван"]
