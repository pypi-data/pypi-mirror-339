"""
Copyright 2022 Inmanta

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contact: code@inmanta.com
"""

import pytest
from tornado.httpclient import AsyncHTTPClient, HTTPClientError, HTTPRequest

from inmanta.server import config


@pytest.mark.asyncio
async def test_web_console_handler(server, inmanta_ui_config):
    base_url = f"http://127.0.0.1:{config.server_bind_port.get()}/console"
    client = AsyncHTTPClient()
    response = await client.fetch(base_url)
    assert response.code == 200

    response = await client.fetch(base_url + "/assets/asset.js")
    assert response.code == 200

    with pytest.raises(HTTPClientError) as exc:
        await client.fetch(base_url + "/assets/not_existing_asset.json")
    assert 404 == exc.value.code

    response = await client.fetch(base_url + "/lsm/catalog")
    assert response.code == 200
    assert "Should be served by default" in response.body.decode("UTF-8")

    # The app should handle the missing view
    response = await client.fetch(base_url + "/lsm/abc")
    assert response.code == 200
    assert "Should be served by default" in response.body.decode("UTF-8")

    # Should handle client side routes that don't start with 'lsm'
    response = await client.fetch(base_url + "/resources")
    assert response.code == 200
    assert "Should be served by default" in response.body.decode("UTF-8")


@pytest.fixture
def inmanta_ui_config_with_auth_enabled(inmanta_ui_config):
    config.Config.set("server", "auth", "True")


@pytest.mark.asyncio
async def test_auth_enabled(inmanta_ui_config_with_auth_enabled, server):
    """
    Ensure that the ui extension doesn't crash if server.auth config option is enabled
    and the server.auth_method is left to its default value.
    """
    base_url = f"http://127.0.0.1:{config.server_bind_port.get()}/console"
    client = AsyncHTTPClient()
    response = await client.fetch(base_url)
    assert response.code == 200


@pytest.mark.asyncio
async def test_start_location_redirect(server, inmanta_ui_config):
    """
    Ensure that the "start" location will redirect to the web console. (issue #202)
    """
    port = config.server_bind_port.get()
    response_url = f"http://localhost:{port}/console/"
    http_client = AsyncHTTPClient()
    request = HTTPRequest(
        url="http://localhost:%s/" % (port),
    )
    response = await http_client.fetch(request, raise_error=False)
    assert response.effective_url == response_url


@pytest.mark.asyncio
async def test_web_console_config(server, inmanta_ui_config):
    base_url = f"http://127.0.0.1:{config.server_bind_port.get()}/console/config.js"
    client = AsyncHTTPClient()
    response = await client.fetch(base_url)
    assert response.code == 200

    assert '\nexport const features = ["A", "B", "C"];' in response.body.decode()

    # test fetching from a deeper path
    base_url = f"http://127.0.0.1:{config.server_bind_port.get()}/console/lsm/config.js"
    client = AsyncHTTPClient()
    response = await client.fetch(base_url)
    assert response.code == 200

    assert '\nexport const features = ["A", "B", "C"];' in response.body.decode()
