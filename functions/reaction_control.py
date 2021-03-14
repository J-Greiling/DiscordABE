'''Bot control via discord emotes'''

__author__ = "Jake Grey"
__date__ = "2021-03"


import discord


class ReactClient(discord.Client):
    def __init__(self, message_id, emote):
        self.message_id = message_id
        self.emote = emote

    async def on_reaction_add(self, payload):
        """calls functions based on reaction emoji"""





