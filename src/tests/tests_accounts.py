import pytest
from shared.utils import Roles


@pytest.mark.django_db
def test_accounts(client, django_user_model):
    # TEST CREATE USER

    users = django_user_model.objects.all()
    assert len(users) == 0

    username = "user2"
    user_password = "LongPassword123"
    user_email = "test@gmail.com"
    user_first_name = "Joe"
    user_last_name = "Doe"
    user_data = {
        "username": username,
        "password": user_password,
        "email": user_email,
        "first_name": user_first_name,
        "last_name": user_last_name,
    }

    username2 = "Alber"
    user_data_no_password = {
        "username": username2,
        "email": user_email,
        "first_name": user_first_name,
        "last_name": user_last_name,
    }
    user_data_no_username = {
        "password": user_password,
        "email": user_email,
        "first_name": user_first_name,
        "last_name": user_last_name,
    }
    user_data_no_email = {
        "username": username2,
        "password": user_password,
        "first_name": user_first_name,
        "last_name": user_last_name,
    }
    user_data_no_first_name = {
        "username": username2,
        "password": user_password,
        "email": user_email,
        "last_name": user_last_name,
    }
    user_data_no_last_name = {
        "username": username2,
        "password": user_password,
        "email": user_email,
        "first_name": user_first_name,
    }

    resp = client.post("/accounts/create/", user_data)
    assert resp.status_code == 201
    assert resp.json()["username"] == username
    assert resp.json()["email"] == user_email

    users = django_user_model.objects.all()
    assert len(users) == 1

    user = django_user_model.objects.get(pk=1)
    assert user.first_name == user_first_name
    assert user.last_name == user_last_name
    assert user.email == user_email
    assert user.groups.all()[0].name == Roles.CLIENT

    resp = client.post("/accounts/create/", user_data)
    assert resp.status_code == 406
    assert resp.json()["error"] == "There is already user with this username."

    resp = client.post("/accounts/create/", user_data_no_password)
    assert resp.status_code == 406
    assert resp.json()["error"] == "Your data is incorrect."

    resp = client.post("/accounts/create/", user_data_no_username)
    assert resp.status_code == 406
    assert resp.json()["error"] == "Your data is incorrect."

    resp = client.post("/accounts/create/", user_data_no_email)
    assert resp.status_code == 406
    assert resp.json()["error"] == "Your data is incorrect."

    resp = client.post("/accounts/create/", user_data_no_last_name)
    assert resp.status_code == 406
    assert resp.json()["error"] == "Your data is incorrect."

    resp = client.post("/accounts/create/", user_data_no_first_name)
    assert resp.status_code == 406
    assert resp.json()["error"] == "Your data is incorrect."

    users = django_user_model.objects.all()
    assert len(users) == 1

    # TEST GET TOKEN

    login_data = {
        "username": username,
        "password": user_password,
    }
    resp = client.post("/accounts/token/", login_data)
    assert resp.status_code == 200
    access_token = resp.json()["access"]
    assert len(access_token) > 0

    wrong_username = "not_user"
    wrong_login_data = {
        "username": wrong_username,
        "password": user_password,
    }

    resp = client.post("/accounts/token/", wrong_login_data)
    assert resp.status_code == 401

    auth_header = {"Authorization": f"Bearer {access_token}"}

    wrong_auth_header = {"Authorization": "Bearer 2"}

    wrong_auth_header_tempalte = {"Authorization": f"Bearer{access_token}"}

    # TEST CHECK PROFILE

    resp = client.get("/accounts/profile/", headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["username"] == username
    assert resp.json()["email"] == user_email
    assert resp.json()["first_name"] == user_first_name
    assert resp.json()["last_name"] == user_last_name

    resp = client.get("/accounts/profile/", headers=wrong_auth_header)
    assert resp.status_code == 401

    resp = client.get("/accounts/profile/", headers=wrong_auth_header_tempalte)
    assert resp.status_code == 401
