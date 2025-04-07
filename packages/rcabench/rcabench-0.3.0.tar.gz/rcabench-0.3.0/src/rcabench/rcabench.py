from typing import Any, AsyncGenerator, Dict, List, Optional
from .api import Algorithm, Dataset, Evaluation, Injection
from .client.async_client import AsyncSSEClient, ClientManager
from .client.http_client import HttpClient
from contextlib import asynccontextmanager
import aiohttp
import asyncio
import requests


class RCABenchSDK:
    CLIENT_NAME = "SSE-{client_id}"

    def __init__(self, base_url: str, max_connections: int = 10):
        """
        Initialize the SDK with the base URL of the server.

        :param base_url: Base URL of the RCABench server, e.g., "http://localhost:8080"
        """
        self.base_url = base_url.rstrip("/") + "/api/v1"

        client = HttpClient(self.base_url)
        self.algorithm = Algorithm(client)
        self.dataset = Dataset(client)
        self.evaluation = Evaluation(client)
        self.injection = Injection(client)

        self.client_manager = ClientManager()
        self.conn_pool = asyncio.Queue(max_connections)
        self.active_connections = set()
        self.loop = asyncio.get_event_loop()

    def _delete(self, url: str, params: Optional[Dict] = None) -> Any:
        url = f"{self.base_url}{url}"
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json()

    @asynccontextmanager
    async def _get_session(self) -> AsyncGenerator[aiohttp.ClientSession, None]:
        session = await self.conn_pool.get()
        try:
            yield session
        finally:
            await self.conn_pool.put(session)

    async def _create_sse_client(
        self, client_id: str, url: str, keyword: Optional[str]
    ) -> AsyncSSEClient:
        url = f"{self.base_url}{url}"
        return AsyncSSEClient(self.client_manager, client_id, url, keyword)

    async def _stream_client(
        self, client_id: str, url: str, keyword: Optional[str]
    ) -> None:
        retries = 0
        max_retries = 3

        sse_client = await self._create_sse_client(client_id, url, keyword)
        self.active_connections.add(client_id)

        while retries < max_retries:
            try:
                await sse_client.connect()
                break
            except aiohttp.ClientError:
                retries += 1
                await asyncio.sleep(2**retries)

        self.active_connections.discard(client_id)

    async def start_multiple_stream(
        self,
        client_ids: List[str],
        url: str,
        keyword: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """批量启动多个SSE流"""
        for client_id in client_ids:
            asyncio.create_task(
                self._stream_client(client_id, url.format(trace_id=client_id), keyword),
                name=self.CLIENT_NAME.format(client_id=client_id),
            )

        report = await self.client_manager.wait_all(timeout)
        await self._cleanup()

        return report

    async def stop_stream(self, client_id: str):
        """停止指定SSE流"""
        for task in asyncio.all_tasks():
            if task.get_name() == self.CLIENT_NAME.format(client_id=client_id):
                task.cancel()
                break

    async def stop_all_streams(self):
        """停止所有SSE流"""
        for client_id in list(self.active_connections):
            await self.stop_stream(client_id)

    async def _cleanup(self):
        """清理所有资源"""
        await self.stop_all_streams()
        while not self.conn_pool.empty():
            session = await self.conn_pool.get()
            await session.close()
