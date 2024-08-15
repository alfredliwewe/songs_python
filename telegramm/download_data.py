from telethon import TelegramClient
import os

# Define your API ID and Hash
api_id = '20842305'
api_hash = 'd9f519db2091b75b0979523eacca9cae'
channel_username = 'USATopmusic'  # Example: 'channel_name'

# Create a client and connect
client = TelegramClient('session_name', api_id, api_hash)


async def main():
    await client.start()
    async for message in client.iter_messages(channel_username):
        if message.media:
            file_path = await message.download_media()
            print(f'Downloaded {file_path}')


with client:
    client.loop.run_until_complete(main())
