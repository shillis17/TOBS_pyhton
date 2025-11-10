from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio
import os


class TwitchChatBot:
    def __init__(
        self,
        app_id: str | None = None,
        app_secret: str | None = None,
        target_channel: str = "casualchaosttv",
        user_scope: list[AuthScope] | None = None,
    ) -> None:
        # Config
        self.app_id = app_id or os.environ.get("TWITCH_BOT_TOKEN")
        self.app_secret = app_secret or os.environ.get("TWITCH_BOT_SECRET")
        self.target_channel = target_channel
        self.user_scope = user_scope or [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

        # These will be set in setup()
        self.twitch: Twitch | None = None
        self.chat: Chat | None = None

        # later you can inject other dependencies:
        # self.obs = obs_controller

    # ========= Event handlers =========

    async def on_ready(self, ready_event: EventData):
        print('Bot is ready for work, joining channels')
        # join our target channel, if you want to join multiple, either call join for each individually
        # or even better pass a list of channels as the argument
        await ready_event.chat.join_room(self.target_channel)
        # you can do other bot initialization things in here

    async def on_message(self, msg: ChatMessage):
        print(f"in {msg.room.name}, {msg.user.name} said: {msg.text}")
        # later: forward to OBS overlay, log to file, trigger effects, etc.

    async def on_sub(self, sub: ChatSub):
        print(
            f"New subscription in {sub.room.name}:\n"
            f"  Type: {sub.sub_plan}\n"
            f"  Message: {sub.sub_message}"
        )
        # later: show alert on stream, play sound, etc.

    async def on_reply_command(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("you did not tell me what to reply with")
        else:
            await cmd.reply(f"{cmd.user.name}: {cmd.parameter}")

    # ========= Setup / lifecycle =========

    async def setup(self):
        """Create Twitch + Chat clients and register events/commands."""
        if not self.app_id or not self.app_secret:
            raise RuntimeError("APP_ID or APP_SECRET not set")

        # Twitch API / auth
        self.twitch = await Twitch(self.app_id, self.app_secret)
        auth = UserAuthenticator(self.twitch, self.user_scope)
        token, refresh_token = await auth.authenticate()
        await self.twitch.set_user_authentication(token, self.user_scope, refresh_token)

        # Chat client
        self.chat = await Chat(self.twitch)

        # Event registrations
        self.chat.register_event(ChatEvent.READY, self.on_ready)
        self.chat.register_event(ChatEvent.MESSAGE, self.on_message)
        self.chat.register_event(ChatEvent.SUB, self.on_sub)

        # Commands
        self.chat.register_command("reply", self.on_reply_command)

    async def run(self):
        """Start the chat bot and keep it alive until user stops it."""
        await self.setup()
        assert self.chat is not None
        assert self.twitch is not None

        self.chat.start()

        try:
            input("press ENTER to stop\n")
        finally:
            self.chat.stop()
            await self.twitch.close()


if __name__ == "__main__":
    bot = TwitchChatBot()
    asyncio.run(bot.run())
