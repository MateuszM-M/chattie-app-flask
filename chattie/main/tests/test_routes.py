import pytest
from flask_login import login_user, current_user
from flask_login import FlaskLoginClient



def test_home_unlogged(client):
    response = client.get("/",
                        follow_redirects=True)
    assert len(response.history) == 1
    assert response.request.path == "/login"


# @pytest.mark.usefixtures('logged_in_user')
# def test_home_logged_in(auth, client, user1):
#     breakpoint()
#     response = client.get("/",
#                         follow_redirects=True)
#     assert response.status_code == 200
#     assert response.request.path == "/"
