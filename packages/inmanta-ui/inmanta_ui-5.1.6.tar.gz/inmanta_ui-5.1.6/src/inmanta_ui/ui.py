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

import json
import logging
import os
from typing import cast

from tornado import routing, web

from inmanta.server import SLICE_SERVER, SLICE_TRANSPORT
from inmanta.server import config as opt
from inmanta.server import extensions, protocol
from inmanta.server.protocol import ServerSlice
from inmanta.server.server import Server
from inmanta_ui.const import SLICE_UI

from .config import oidc_auth_url, oidc_client_id, oidc_realm, web_console_enabled, web_console_features, web_console_path

composer = extensions.BoolFeature(
    slice=SLICE_UI,
    name="smart_composer",
    description="Enable the smart composer in the web console.",
)


LOGGER = logging.getLogger(__name__)


class UISlice(ServerSlice):
    def __init__(self) -> None:
        super().__init__(SLICE_UI)

    async def prestart(self, server: protocol.Server) -> None:
        _server = cast(Server, server.get_slice(SLICE_SERVER))
        self.add_web_console_handler(_server)
        await super().prestart(server)

    async def start(self) -> None:
        await super().start()

    async def prestop(self) -> None:
        await super().prestop()

    async def stop(self) -> None:
        await super().stop()

    def get_dependencies(self) -> list[str]:
        return [SLICE_SERVER]

    def get_depended_by(self) -> list[str]:
        # Ensure we are started before the HTTP endpoint becomes available
        return [SLICE_TRANSPORT]

    def define_features(self) -> list[extensions.Feature]:
        return [composer]

    def add_web_console_handler(self, server: Server) -> None:
        if not web_console_enabled.get():
            LOGGER.info("The web-console is disabled.")
            return

        path = web_console_path.get()
        if not os.path.isdir(path):
            raise Exception(f"The web-ui.console_path config option references the non-existing directory {path}.")
        LOGGER.info("Serving the web-console from %s", path)

        config_js_content = ""
        if opt.server_enable_auth.get():
            server_auth_method: str = opt.server_auth_method.get()
            if server_auth_method == "oidc":
                config_js_content = f"""
                    window.auth = {{
                        'method': 'oidc',
                        'realm': '{oidc_realm.get()}',
                        'url': '{oidc_auth_url.get()}',
                        'clientId': '{oidc_client_id.get()}',
                    }};\n"""
            elif server_auth_method == "database":
                config_js_content = """
                    window.auth = {
                        'method': 'database',
                    };\n"""
            elif server_auth_method == "jwt":
                config_js_content = """
                    window.auth = {
                        'method': 'jwt',
                    };\n"""
            else:
                raise Exception(
                    f"Invalid value for config option server.auth_method: {opt.server_auth_method.get()}. "
                    "Expected either 'oidc' or 'database'."
                )

        config_js_content += f"\nexport const features = {json.dumps(web_console_features.get())};\n"

        server.add_static_content(r"/console/(.*)config.js", content=config_js_content)
        location = "/console/"
        options = {"path": path, "default_filename": "index.html"}
        server._handlers.append(
            routing.Rule(
                routing.PathMatches(r"%s(.*\.\w{2,5}$)" % location),
                FlatFileHandler,
                options,
            )
        )
        server._handlers.append(
            routing.Rule(routing.PathMatches(r"%s" % location[:-1]), web.RedirectHandler, {"url": location[1:]})
        )
        server._handlers.append(
            routing.Rule(
                routing.PathMatches(r"%s(.*)" % location), SingleFileHandler, {"path": os.path.join(path, "index.html")}
            )
        )
        self._handlers.append((r"/", web.RedirectHandler, {"url": location[1:]}))


class SingleFileHandler(web.StaticFileHandler):
    """Always serves the single file given in the path option, useful for single page applications with client-side routing"""

    @classmethod
    def get_absolute_path(cls, root, path):
        return web.StaticFileHandler.get_absolute_path(root, "")


class FlatFileHandler(web.StaticFileHandler):
    """Always serves files from the root folder, useful when using a proxy"""

    @classmethod
    def get_absolute_path(cls, root, path):
        parts = os.path.split(path)
        if parts:
            return web.StaticFileHandler.get_absolute_path(root, parts[-1])
        return web.StaticFileHandler.get_absolute_path(root, "")
