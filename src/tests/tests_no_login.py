import pytest


@pytest.mark.django_db
def test_products(client):
    #
    resp = client.get("/products/list/")
    assert resp.status_code == 200

    resp = client.get("/products/create/")
    assert resp.status_code == 401

    resp = client.get("/products/1/")
    assert resp.status_code == 404

    resp = client.get("/products/1/delete/")
    assert resp.status_code == 401

    resp = client.get("/products/1/update/")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_orders(client):
    resp = client.get("/orders/create/")
    assert resp.status_code == 401

    resp = client.get("/orders/statistics/")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_categories(client):
    resp = client.get("/categories/list/")
    assert resp.status_code == 200

    resp = client.get("/categories/create/")
    assert resp.status_code == 401

    resp = client.get("/categories/1/")
    assert resp.status_code == 404

    resp = client.get("/categories/1/delete/")
    assert resp.status_code == 401

    resp = client.get("/categories/1/update/")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_accounts(client):
    resp = client.post("/accounts/token/")
    assert resp.status_code == 400

    resp = client.post("/accounts/token/refresh/")
    assert resp.status_code == 400

    resp = client.post("/accounts/create/")
    assert resp.status_code == 406

    resp = client.get("/accounts/profile/")
    assert resp.status_code == 401

    resp = client.get("/accounts/profile/orders/")
    assert resp.status_code == 401

    resp = client.get("/accounts/profile/wishlist/list/")
    assert resp.status_code == 401

    resp = client.get("/accounts/profile/wishlist/add/1/")
    assert resp.status_code == 401

    resp = client.delete("/accounts/profile/wishlist/remove/1/")
    assert resp.status_code == 401
