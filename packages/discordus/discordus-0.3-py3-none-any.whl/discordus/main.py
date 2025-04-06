import discord
from discord import app_commands
from typing import Callable, List, Tuple

# Global variables
server_id_client = None
token_client = None
commands_list = []
client = None

__all__ = ["preset_bot", "send_message", "add_command", "run_client", "testAppPrints", "channel_send", "direct_message"]

def preset_bot(server_id: int, token: str):
    global server_id_client, token_client
    server_id_client = server_id
    token_client = token

async def channel_send(channel_id: int, message: str):
    global client
    if client:
        channel = client.get_channel(channel_id)
        if channel:
            await channel.send(message)
        else:
            print(f"Channel {channel_id} not found.")
    else:
        raise RuntimeError("Client not initialized.")

async def direct_message(user_id: int, message: str):
    global client
    if client:
        user = await client.fetch_user(user_id)
        if user:
            try:
                dm = await user.create_dm()
                await dm.send(message)
            except Exception as e:
                print(f"DM failed: {e}")
        else:
            print(f"User {user_id} not found.")
    else:
        raise RuntimeError("Client not initialized.")

async def send_message(interaction: discord.Interaction, text: str, ephemeral: bool = False):
    await interaction.response.send_message(content=text, ephemeral=ephemeral)

def add_command(
    name: str,
    description: str,
    response: Callable[[discord.Interaction, dict], None],
    options: List[Tuple[str, str, type]] = [],
):
    commands_list.append((name, description, response, options))

def testAppPrints():
    print("Server ID:", server_id_client or "Not set")
    print("Token:", token_client[:10] + "..." if token_client else "Not set")

def run_client():
    global client
    if not server_id_client or not token_client:
        raise ValueError("Use preset_bot() before run_client()")

    class AClient(discord.Client):
        def __init__(self):
            super().__init__(intents=discord.Intents.default())
            self.tree = app_commands.CommandTree(self)
            self.synced = False

        async def setup_hook(self):
            for name, description, response, options in commands_list:
                if options:
                    # Currently support only one str argument (can be extended)
                    def make_func(resp):
                        async def command_func(interaction: discord.Interaction, message: str):
                            await resp(interaction, {"message": message})
                        return command_func

                    cmd_func = make_func(response)

                    self.tree.command(
                        name=name,
                        description=description,
                        guild=discord.Object(id=server_id_client)
                    )(app_commands.describe(message=options[0][1])(cmd_func))

                else:
                    def make_func(resp):
                        async def command_func(interaction: discord.Interaction):
                            await resp(interaction, {})
                        return command_func

                    cmd_func = make_func(response)

                    self.tree.command(
                        name=name,
                        description=description,
                        guild=discord.Object(id=server_id_client)
                    )(cmd_func)

            if not self.synced:
                await self.tree.sync(guild=discord.Object(id=server_id_client))
                self.synced = True

    client = AClient()

    @client.event
    async def on_ready():
        print(f"✅ Logged in as {client.user}")

    try:
        client.run(token_client)
    except discord.LoginFailure:
        print("❌ Invalid token.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
