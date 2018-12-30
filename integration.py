import configparser
import discord
import asyncio

config = configparser.ConfigParser()

config.read('config.ini')

TOKEN = config['DEFAULT'].get('token')
SERVER_ID = config['DEFAULT'].get('id')
TEST_USERS = {'Raúl Morales Hidalgo#8627': 'Raúl Morales Hidalgo',
              'asierrayk#3400': 'Asier Cardoso Sánchez',
              'Alberto Masó Molina#2925': 'Alberto Masó Molina',
              'AlexO#2487': 'Alexander Olleta del Molino'}

# create discord client
client = discord.Client()

# bot is ready
@client.event
async def on_ready():
    try:
        print(client.user.name)
        print(client.user.id)
        print('Discord.py Version: {}'.format(discord.__version__))

        s = SociosIntegration(client, SERVER_ID)
        await s.sync_socios(TEST_USERS)

    except Exception as e:
        print(e)

class SociosIntegration():
    def __init__(self, client, server_id):
        self.client = client
        self.server = client.get_server(server_id)
        self.socio_role = discord.utils.get(self.server.roles, name="socio")


    async def sync_socios(self, socios_name):
        discord_socios = self.get_socios()
        socios = self.get_members(socios_name.keys())
        print(socios)
        print(discord_socios)

        to_add = set(socios) - set(discord_socios)
        to_remove = set(discord_socios) - set(socios)

        for socio in socios:
            identifier = socios_name['{}#{}'.format(socio.name, socio.discriminator)]
            print(identifier)
            # await self.change_nickname(socio, identifier)


        print('add', to_add)
        for member in to_add:
            print(member)
            await self.add_socio(member)

        print('remove', to_remove)
        for member in to_remove:
            print(member)
            await self.remove_socio(member)

    def get_members(self, member_names):
        members = []
        for full_name in member_names:
            name, discriminator = full_name.split('#')
            m = discord.utils.get(self.server.members, name=name, discriminator=discriminator)
            members.append(m)
        return members

    def get_socios(self):
        members = self.client.get_all_members()
        socios = []
        for m in members:
            if 'socio' in [r.name for r in m.roles]:
                socios.append(m)

        return socios

    async def add_socio(self, member):
        try:
            await self.client.add_roles(member, self.socio_role)
        except Exception as e:
            print(e)
            raise(e)

    async def remove_socio(self, member):
        try:
            await self.client.remove_roles(member, self.socio_role)
        except Exception as e:
            print(e)
            raise(e)

    async def change_nickname(self, member, name):
        await self.client.change_nickname(member, name)

# start bot
client.run(TOKEN)
