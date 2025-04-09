from asyncio import run, sleep
from io import BytesIO
from urllib.parse import parse_qs

from aiogram import Bot
from pyrogram import Client
from pyrogram.errors import UserNotParticipant
from pyrogram.raw import functions
from pyrogram.raw.base.upload import File
from pyrogram.raw.functions.messages import UploadMedia
from pyrogram.raw.functions.photos import GetUserPhotos
from pyrogram.raw.functions.upload import GetFile
from pyrogram.raw.types import (
    InputPeerSelf,
    InputMediaUploadedDocument,
    MessageMediaDocument,
    InputMediaUploadedPhoto,
    MessageMediaPhoto,
    InputDocumentFileLocation,
    InputPhotoFileLocation,
)
from pyrogram.raw.types.photos import Photos
from pyrogram.types import Chat, ChatPrivileges
from x_model import init_db
from xync_client.loader import TG_API_ID, TG_API_HASH, PG_DSN
from xync_schema import models
from xync_schema.models import Agent


class PyroClient:
    max_privs = ChatPrivileges(
        can_manage_chat=True,  # default
        can_delete_messages=True,
        can_delete_stories=True,  # Channels only
        can_manage_video_chats=True,  # Groups and supergroups only
        can_restrict_members=True,
        can_promote_members=True,
        can_change_info=True,
        can_post_messages=True,  # Channels only
        can_post_stories=True,  # Channels only
        can_edit_messages=True,  # Channels only
        can_edit_stories=True,  # Channels only
        can_invite_users=True,
        can_pin_messages=True,  # Groups and supergroups only
        can_manage_topics=True,  # Supergroups only
        is_anonymous=True,
    )

    def __init__(self, ab: Agent | Bot):
        name = str(ab.actor.person.user.id) if isinstance(ab, Agent) else str(ab.id)
        auth = {"session_string": ab.auth["sess"]} if isinstance(ab, Agent) else {"bot_token": ab.token}
        self.app: Client = Client(name, TG_API_ID, TG_API_HASH, **auth)

    async def get_init_data(self) -> dict:
        async with self.app as app:
            app: Client
            bot = await app.resolve_peer("wallet")
            res = await app.invoke(functions.messages.RequestWebView(peer=InputPeerSelf(), bot=bot, platform="ios"))
            raw = parse_qs(res.url)["tgWebAppUserId"][0].split("#tgWebAppData=")[1]
            j = parse_qs(raw)
            return {
                "web_view_init_data": {
                    "query_id": j["query_id"][0],
                    "user": j["user"][0],
                    "auth_date": j["auth_date"][0],
                    "hash": j["hash"][0],
                },
                "web_view_init_data_raw": raw,
                "ep": "menu",
            }

    async def create_orders_forum(self, uid: str | int) -> tuple[int, bool]:
        async with self.app as app:
            app: Client
            await app.get_me()
            chat: Chat = await app.create_supergroup("Xync Orders", "Xync Orders")
            if not (await app.toggle_forum_topics(chat_id=chat.id, enabled=True)):
                await app.delete_channel(chat.id)
                await chat.leave()
                raise Exception(f"Chat {chat.id} for {app.me.username} not converted to forum")
            await chat.add_members(["XyncNetBot"])  # , "xync_bot"
            await chat.promote_member("XyncNetBot", self.max_privs)
            added = await chat.add_members([uid])
            try:
                await sleep(1, await chat.get_member(uid))
            except UserNotParticipant:
                added = False
            # await chat.leave()
            return chat.id, added

    async def get_user_photos(self, uid: str | int) -> Photos:
        async with self.app as app:
            app: Client
            try:
                peer = await app.resolve_peer(uid)
            except Exception as e:
                raise e
            return await app.invoke(GetUserPhotos(user_id=peer, offset=0, limit=1, max_id=-1))

    async def send_message(self, uid, txt):
        async with self.app as app:
            app: Client
            try:
                return await app.send_message(uid, txt)
            except Exception as e:
                raise e

    async def save_file(self, byts: bytes, ctype: str) -> tuple[MessageMediaDocument, bytes]:
        async with self.app as app:
            in_file = await app.save_file(BytesIO(byts))
            imud = InputMediaUploadedDocument(file=in_file, mime_type=ctype, attributes=[])
            upf: MessageMediaDocument = await app.invoke(UploadMedia(peer=InputPeerSelf(), media=imud))
            return upf, (
                upf.document.id.to_bytes(8, "big")
                + upf.document.access_hash.to_bytes(8, "big", signed=True)
                + upf.document.file_reference
            )

    @staticmethod
    def ref_enc(ph_id: int, access_hash: int, ref: bytes) -> bytes:
        return ph_id.to_bytes(8, "big") + access_hash.to_bytes(8, "big", signed=True) + ref

    @staticmethod
    def ref_dec(full_ref: bytes) -> tuple[int, int, bytes]:
        pid, ah = int.from_bytes(full_ref[:8], "big"), int.from_bytes(full_ref[8:16], "big", signed=True)
        return pid, ah, full_ref[16:]

    async def save_photo(self, file: bytes) -> tuple[MessageMediaPhoto, bytes]:
        async with self.app as app:
            in_file = await app.save_file(BytesIO(file))
            upm = UploadMedia(peer=InputPeerSelf(), media=InputMediaUploadedPhoto(file=in_file))
            upp: MessageMediaPhoto = await app.invoke(upm)
            return upp, self.ref_enc(upp.photo.id, upp.photo.access_hash, upp.photo.file_reference)

    async def get_file(self, fid: bytes) -> File:
        async with self.app as app:
            pid, ah, ref = self.ref_dec(fid)
            loc = InputDocumentFileLocation(id=pid, access_hash=ah, file_reference=ref, thumb_size="x")
            return await app.invoke(GetFile(location=loc, offset=0, limit=512 * 1024))

    async def get_photo(self, fid: bytes, st: str) -> File:
        async with self.app as app:
            pid, ah, ref = self.ref_dec(fid)
            loc = InputPhotoFileLocation(id=pid, access_hash=ah, file_reference=ref, thumb_size=st)
            return await app.invoke(GetFile(location=loc, offset=0, limit=512 * 1024))


async def main():
    _ = await init_db(PG_DSN, models, True)
    agent: Agent = await Agent.filter(auth__isnull=False, ex__name="TgWallet").prefetch_related("ex").first()
    pcl = PyroClient(agent)
    await pcl.create_orders_forum(agent.actor.user_id)


if __name__ == "__main__":
    run(main())
