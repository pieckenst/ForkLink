Forklink
================
Welcome to Forklink's Documentation. Forklink is a robust and powerful Lavalink wrapper for disnake.

Support
---------------------------
For support using Forklink, please join the official `support server
<http://discord.gg/RAKc3HF>`_ on `Discord <https://discordapp.com/>`_.

Installation
---------------------------
The following commands are currently the valid ways of installing forklink.

**Forklink requires Python 3.7+**

**Windows**

.. code:: sh

    py -3.7 -m pip install Forklink

**Linux**

.. code:: sh

    python3.7 -m pip install Forklink

Getting Started
----------------------------

A quick and easy bot example:

.. code:: py

    import discord
    import Forklink
    from discord.ext import commands


    class Bot(commands.Bot):

        def __init__(self):
            super(Bot, self).__init__(command_prefix=['audio ', 'wave ','aw '])

            self.add_cog(Music(self))

        async def on_ready(self):
            print(f'Logged in as {self.user.name} | {self.user.id}')


    class Music(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

            if not hasattr(bot, 'Forklink'):
                self.bot.Forklink = forklink.Client(bot=self.bot)

            self.bot.loop.create_task(self.start_nodes())

        async def start_nodes(self):
            await self.bot.wait_until_ready()

            # Initiate our nodes. For this example we will use one server.
            # Region should be a disnake guild.region e.g sydney or us_central (Though this is not technically required)
            await self.bot.forklink.initiate_node(host='0.0.0.0',
                                                  port=2333,
                                                  rest_uri='http://0.0.0.0:2333',
                                                  password='youshallnotpass',
                                                  identifier='TEST',
                                                  region='us_central')

        @commands.command(name='connect')
        async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
            if not channel:
                try:
                    channel = ctx.author.voice.channel
                except AttributeError:
                    raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

            player = self.bot.forklink.get_player(ctx.guild.id)
            await ctx.send(f'Connecting to **`{channel.name}`**')
            await player.connect(channel.id)

        @commands.command()
        async def play(self, ctx, *, query: str):
            tracks = await self.bot.forklink.get_tracks(f'ytsearch:{query}')

            if not tracks:
                return await ctx.send('Could not find any songs with that query.')

            player = self.bot.forklink.get_player(ctx.guild.id)
            if not player.is_connected:
                await ctx.invoke(self.connect_)

            await ctx.send(f'Added {str(tracks[0])} to the queue.')
            await player.play(tracks[0])


    bot = Bot()
    bot.run('TOKEN')

Client
----------------------------

.. autoclass:: forklink.client.Client
    :members:


Node
----------------------------

.. autoclass:: forklink.node.Node
    :members:


Player
----------------------------
.. autoclass:: forklink.player.Player
    :members:


Track
----------------------------
.. autoclass:: forklink.player.Track
    :members:

.. autoclass:: forklink.player.TrackPlaylist
    :members:


Equalizer
----------------------------
.. autoclass:: forklink.eqs.Equalizer
    :members:


Event Payloads
----------------------------

.. autoclass:: forklink.events.TrackStart
    :members:

.. autoclass:: forklink.events.TrackEnd
    :members:

.. autoclass:: forklink.events.TrackException
    :members:

.. autoclass:: forklink.events.TrackStuck
    :members:


ForklinkMixin
-----------------------

.. warning::
    Listeners must be used with a `forklink.ForklinkMixin.listener()` decorator to work.

.. warning::
    Listeners must be coroutines.

.. autoclass:: forklink.meta.ForklinkMixin
    :members:


Errors
-----------------------

.. autoexception:: forklink.errors.ForklinkException

.. autoexception:: forklink.errors.NodeOccupied

.. autoexception:: forklink.errors.InvalidIDProvided

.. autoexception:: forklink.errors.ZeroConnectedNodes

.. autoexception:: forklink.errors.AuthorizationFailure
