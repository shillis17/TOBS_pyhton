from twitchController import TwitchChatBot
from obsController import ObsController
import asyncio

if __name__ == "__main__":
    obsctl = ObsController()
    print(obsctl.get_version())
    print(f"Scenes found: {obsctl.get_scenes()}")
    print(f"Video Sources found: {obsctl.get_sources()}")
    print(f"Audio Sources found: {obsctl.get_input_names()}")

    bot = TwitchChatBot()
    asyncio.run(bot.run())
