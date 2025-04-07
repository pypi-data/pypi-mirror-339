from typing import Annotated

import pytest

from lihil import Lihil, Route, Text
from lihil.plugins.auth.oauth import OAuth2PasswordFlow, OAuthLoginForm
from lihil.plugins.testclient import LocalClient


async def test_login():
    users = Route("users")
    token = Route("token")

    async def get_user(
        name: str, token: Annotated[str, OAuth2PasswordFlow(token_url="token")]
    ):
        return token

    async def create_token(credentials: OAuthLoginForm) -> Text:
        return "ok"

    users.get(get_user)
    token.post(create_token)

    form_ep = token.get_endpoint("POST")
    form_ep.setup()

    lc = LocalClient()
    res = await lc.submit_form(
        form_ep, form_data={"username": "user", "password": "pass"}
    )

    assert res.status_code == 200
    assert await res.text() == "ok"

    # lhl = Lihil(routes=[users, token])


def test_random_obj_to_jwt(): ...
