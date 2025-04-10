# Copyright 2025 IBM Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from copy import deepcopy

import beeai_cli.commands.agent
import beeai_cli.commands.compose
import beeai_cli.commands.env
import beeai_cli.commands.telemetry
import beeai_cli.commands.tool
from beeai_cli.async_typer import AsyncTyper
from beeai_cli.configuration import Configuration

logging.basicConfig(level=logging.INFO if Configuration().debug else logging.FATAL)

app = AsyncTyper(no_args_is_help=True)
app.add_typer(beeai_cli.commands.tool.app, name="tool", no_args_is_help=True, help="Manage tools.")
app.add_typer(beeai_cli.commands.env.app, name="env", no_args_is_help=True, help="Manage environment variables.")
app.add_typer(beeai_cli.commands.agent.app, name="agent", no_args_is_help=True, help="Manage agents.")
app.add_typer(beeai_cli.commands.telemetry.app, name="telemetry", no_args_is_help=True, help="Configure telemetry.")
app.add_typer(beeai_cli.commands.compose.app, name="compose", no_args_is_help=True, help="Manage agent composition.")


agent_alias = deepcopy(beeai_cli.commands.agent.app)
for cmd in agent_alias.registered_commands:
    cmd.rich_help_panel = "Agent commands"

app.add_typer(agent_alias, name="", no_args_is_help=True)


@app.command("serve")
async def serve():
    """Start server."""
    import beeai_server

    beeai_server.serve()


@app.command("ui")
async def ui():
    """Launch graphical interface."""
    import webbrowser
    import httpx

    host_url = str(Configuration().host)

    # Failure here will trigger the automatic service start mechanism
    async with httpx.AsyncClient() as client:
        await client.head(host_url)

    await beeai_cli.commands.env.ensure_llm_env()
    webbrowser.open(host_url)


if __name__ == "__main__":
    app()
