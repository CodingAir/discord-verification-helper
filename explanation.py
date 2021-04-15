import asyncio

import discord


class Message:
    def __init__(self, client, promote_channel):
        self.client = client
        self.promote_channel = promote_channel
        self.explanation_message = None

    async def update_explanation(self, channel):
        if self.explanation_message is not None:
            await asyncio.sleep(5)
            await self.explanation_message.delete()
            await asyncio.sleep(.5)

        content = "Just enter your **SpigotMC username** in this chat.\n\n" \
                  "You will get a verification number via SpigotMC which then have to be confirmed in this channel."

        embed = discord.Embed(description=content, colour=0x327fa8)
        embed.set_author(name="How to verify", icon_url="https://i.imgur.com/ZoSmsVs.png")

        self.explanation_message = await channel.send(embed=embed)

    async def on_ready(self):
        channel = await self.__has_old_explanation__()
        if channel is not None:
            await self.update_explanation(channel)

    # Returns a channel if there is no explanation in the last 10 messages.
    async def __has_old_explanation__(self):
        # assumes that the bot is only connected to one guild
        channel = await self.client.fetch_channel(self.promote_channel)

        if channel is not None:
            for message in await channel.history(limit=10).flatten():
                for embed in message.embeds:
                    if embed.author.name == "How to verify":
                        self.explanation_message = message
                        return None
        return channel