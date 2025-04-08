from event_source import Client
import asyncio
import aiohttp
import json
import time


def print_event(event):
    print(event)


async def main():
    client = Client(
        "http://localhost:8080/sse",
        print_event,
        param={"name": "dilanka"},
        # headers={"authorization": "Bearer token"},
    )
    read_task = asyncio.create_task(listen(client))
    # client.connect_v2()
    await asyncio.sleep(5)
    await client.close()
    await read_task


async def listen(client):
    await client.connect()


if __name__ == "__main__":
    asyncio.run(main())


# import aiohttp
# import asyncio


# async def fetch_stream():
#     async with aiohttp.ClientSession() as session:
#         try:
#             async with session.get("http://localhost:8080/sse") as response:
#                 stream = response.content

#                 # Create a task to read the stream
#                 read_task = asyncio.create_task(read_stream(stream))

#                 # Wait for 5 seconds before cancelling
#                 await asyncio.sleep(5)
#                 read_task.cancel()

#                 try:
#                     await read_task
#                 except asyncio.CancelledError:
#                     print("Stream reading cancelled after 5 seconds.")

#         except Exception as e:
#             print(f"Exception: {e}")


# async def read_stream(stream):
#     async for line in stream:
#         print(line)


# asyncio.run(fetch_stream())
