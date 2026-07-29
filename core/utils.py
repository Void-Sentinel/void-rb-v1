import aiohttp


async def send_message_http(session: aiohttp.ClientSession, application_id: int, interaction_token: str, content: str):
    url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}"
    payload = {"content": content, "allowed_mentions": {"parse": ["everyone", "users", "roles"]}}
    async with session.post(url, json=payload) as resp:
        try:
            data = await resp.json()
        except Exception:
            data = {}
        return resp.status, data


async def delete_message_http(session: aiohttp.ClientSession, application_id: int, interaction_token: str, message_id: int):
    url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}/messages/{message_id}"
    async with session.delete(url) as resp:
        return resp.status
