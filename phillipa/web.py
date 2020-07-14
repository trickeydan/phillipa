"""Web stuff."""

import asyncio
import logging
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Dict

from aiohttp import web
from discord.ext.commands import Cog

from phillipa.emoji import HEART

if TYPE_CHECKING:
    from .phillipa import PhillipaBot

LOGGER = logging.getLogger(__name__)


class WebPhillipa(Cog):  # type: ignore
    """Phillipa on the web."""

    def __init__(self, bot: "PhillipaBot"):
        self.bot = bot

    async def root_handler(self, request: web.Request) -> web.Response:
        """Homepage."""
        return web.Response(text=HEART)

    async def webserver(self, port: int = 8999) -> None:
        """Run a webserver."""
        app = web.Application()

        routes: Dict[
            str, Callable[[web.Request], Coroutine[Any, Any, web.Response]],
        ] = {
            "/": self.root_handler,
        }

        for route, handler in routes.items():
            app.router.add_get(route, handler)
            LOGGER.info(f"Registered handler for {route}")

        runner = web.AppRunner(app)
        await runner.setup()
        LOGGER.info(f"Starting website on {port}")
        self.site = web.TCPSite(runner, "0.0.0.0", port)
        LOGGER.info("Waiting for Discord connection")
        await self.bot.wait_until_ready()
        LOGGER.info("Web now available")
        await self.site.start()

    def __unload(self) -> None:
        asyncio.ensure_future(self.site.stop())
