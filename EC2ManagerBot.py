import discord
import requests

# YOUR OWN DISCORD BOT TOKEN
TOKEN = 'AAAAAAAAAAAAAAAAAAAAAAAA.AAAAAA.AAAA_AAAAAAAAAAAAAAAAAAAAA'

# YOUR OWN DISCORD CHANNEL ID
ID_CHANNEL_BOT = 000000000000000000

EMOJI_EC2_DOWN = 'ec2_down'
EMOJI_EC2_UP_COMMON = 'ec2_up_common'
EMOJI_EC2_UP_BOOST = 'ec2_up_boost'

EC2_INSTANCE_TYPE_POOR = 't3a.large'
EC2_INSTANCE_TYPE_GOOD = 'm5n.large'

LAMBDA_INVOKE_PATH = 'https://${YOUR_OWN_APIGW_PATH}/dev/ec2'

STATUS_OK = 200

client = discord.Client()


async def down_ec2(user_name):
    channel = client.get_channel(ID_CHANNEL_BOT)
    r = requests.get(f'{LAMBDA_INVOKE_PATH}/down').json()

    status = r["statusCode"]

    if status == STATUS_OK:
        await channel.send(f'ec2 down down down ... by `{user_name}`')
    else:
        await channel.send(f'[ERROR!] lambda invocation error --> `{r["body"]}`')


async def up_ec2(user_name, ec2_instance_type):
    channel = client.get_channel(ID_CHANNEL_BOT)
    r = requests.get(
        f'{LAMBDA_INVOKE_PATH}/up?instance_type={ec2_instance_type}'
    ).json()

    status = r["statusCode"]

    if status == STATUS_OK:
        await channel.send(f'ec2 up up up ... by `{user_name}`\ninstance type is `{ec2_instance_type}`')
    else:
        await channel.send(f'[ERROR!] lambda invocation error --> `{r["body"]}`')


async def validate_message(message):
    if message.author.bot:
        return

    channel_id = message.channel.id
    if channel_id != ID_CHANNEL_BOT:
        return

    content = message.content
    author = message.author.name

    if EMOJI_EC2_DOWN in content:
        await down_ec2(author)
        return

    if EMOJI_EC2_UP_COMMON in content:
        await up_ec2(author, EC2_INSTANCE_TYPE_POOR)
        return

    if EMOJI_EC2_UP_BOOST in content:
        await up_ec2(author, EC2_INSTANCE_TYPE_GOOD)
        return


async def validate_reaction(payload):
    channel_id = payload.channel_id
    if channel_id != ID_CHANNEL_BOT:
        return

    emoji = payload.emoji.name
    author = payload.member

    if emoji == EMOJI_EC2_DOWN:
        await down_ec2(author)
        return

    if emoji == EMOJI_EC2_UP_COMMON:
        await up_ec2(author, EC2_INSTANCE_TYPE_POOR)
        return

    if emoji == EMOJI_EC2_UP_BOOST:
        await up_ec2(author, EC2_INSTANCE_TYPE_GOOD)
        return


@client.event
async def on_ready():
    channel = client.get_channel(ID_CHANNEL_BOT)
    await channel.send('hello!')


@client.event
async def on_message(message):
    await validate_message(message)


@client.event
async def on_raw_reaction_add(payload):
    await validate_reaction(payload)


client.run(TOKEN)
