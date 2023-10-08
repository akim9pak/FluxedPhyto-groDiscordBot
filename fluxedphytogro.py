import discord
from bot_logic import gen_pass, gen_coin

# Переменная intents - хранит привилегии бота
intents = discord.Intents.default()
# Включаем привелегию на чтение сообщений
intents.message_content = True
# Создаем бота в переменной client и передаем все привелегии
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    print(1)
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send("Hi!")
    if message.content.startswith('$password'):
        await message.channel.send(gen_pass(10))
    if message.content.startswith('$coinflip'):
        await message.channel.send(gen_coin())
    if message.content.startswith('$meme'):
        skibidi = str(random.randint(1,3))    
        with open('images/mem'+ skibidi + '.jpg', 'rb') as f:
            picture = discord.File(f)
        await message.channel.send(file=picture)
    if message.content.startswith('$duck'):
        image_url = get_duck_image_url()
        await message.channel.send(image_url)
    if message.content.startswith('$dice'):
        first_dice = random.randint(1, 6)
        second_dice = random.randint(1, 6)
        await message.channel.send(f'Первый кубик - {first_dice}, Второй кубик - {second_dice}')
    if message.content.startswith('$trash'):
        with open('trash.png', 'rb') as f:
            trash_picture = discord.File(f)
        await message.channel.send(file=trash_picture)
    elif message.content.startswith('$bye'):
        await message.channel.send("Bye!")

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.role_message_id = 1155442002779975721  # ID of the message that can be reacted to to add/remove a role.
        self.emoji_to_role = {
            discord.PartialEmoji(name='🔴'): 1155444529579704351,  # ID of the role associated with unicode emoji '🔴'.
            discord.PartialEmoji(name='🟡'): 1155444625423749160,  # ID of the role associated with unicode emoji '🟡'.
            discord.PartialEmoji(name='green', id=0): 0,  # ID of the role associated with a partial emoji's ID.
        }

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally, add the role.
            await payload.member.add_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass


intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)

client.run("darthvaderpon")
