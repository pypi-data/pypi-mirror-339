import asyncio
from abc import ABC
from typing import Optional, Type, Any

import aiohttp
from aiohttp import ClientSession

from ddapi.types import T

try:
    import orjson

    DEFAULT_JSON_DECODER = orjson.loads
except ImportError:
    from aiohttp.typedefs import DEFAULT_JSON_DECODER


class API(ABC):
    def __init__(
            self,
            session: ClientSession = None,
            autoclose: bool = True,
            json_loads: Any = DEFAULT_JSON_DECODER
    ):
        self.__session = session
        self.json_loads = json_loads
        self.autoclose = autoclose

        if self.__session is None:
            self.__session = aiohttp.ClientSession()

    async def __aenter__(self):
        if self.__session is None:
            self.__session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, _exc_type, _exc_val, _exc_tb):
        if self.autoclose:
            await self.close()

    def __del__(self):
        if self.__session is not None and not self.__session.closed:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.close())
            else:
                loop.run_until_complete(self.close())

    async def _get(self, url: str) -> Optional[dict]:
        """Send a GET request to the given URL and return the response as JSON."""
        async with self.__session.get(url) as req:
            return (
                await req.json(loads=self.json_loads)
                if req.status == 200
                else None
            )

    async def _generate_model_instance(
            self,
            url: str,
            model: Type[T],
            k: Optional[str] = None
    ) -> Optional[T]:
        """Generate a model instance from the given URL and optional keyword arguments.

        Args:
            url (str): The URL to fetch data from.
            model (Type[ModelType]): The model class to instantiate.
            k (str, optional): An optional keyword to wrap the data in a dictionary.

        Returns:
            Optional[ModelType]: A model instance.
        """
        dat = await self._get(url)
        if dat is None or not dat:
            return

        data_to_pass = {k: dat} if k is not None else dat
        return model(**data_to_pass)

    async def is_closed(self) -> bool:
        """True is closed, False otherwise."""
        return self.__session is None or self.__session.closed

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self.__session is not None:
            await self.__session.close()
        self.__session = None

    @property
    def domain(self) -> str:
        return "ddnet.org"

    @staticmethod
    def powered() -> None:
        return None
