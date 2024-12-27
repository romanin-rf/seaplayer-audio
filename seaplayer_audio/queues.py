import asyncio
import queue

# ! Sync Queue Class

class Queue(queue.Queue):
    def abort(self) -> None:
        while not self.empty():
            self.get()

# ! Async Queue Class

class AsyncQueue(asyncio.Queue):
    async def abort(self) -> None:
        while not self.empty():
            await self.get()