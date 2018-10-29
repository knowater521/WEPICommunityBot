import discord, os, asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

important_roles = ["Dev", "MEE6", "DISBOARD", "Discordちゃんねる(β)", "STAFF", "BOT", "verify"]

@bot.event
async def on_ready():
    print('ログイン情報')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel("480978992891953152")
    string = member.mention + "さん、うぇぴ ゲーミングコミュニティへようこそ！\n\n #「うぇぴゲーミングコミュニティ」のご案内 には、ルールや必要事項が記載されています。入ったら最初ご覧になるようにお願いします。\n\n*新規の方は #verify にて` !verify`の発言をお願いしております。発言が確認され次第、自動的に他のチャンネルへの接続ができるようになります。*\n\n#自己紹介 は全ユーザーが共通して見ることができるチャンネルです。是非自己紹介をお願いします！\n\n---------------------------"""
    await bot.say(string)

@bot.command(pass_context=True)
async def verify(ctx):
    member = ctx.message.author
    role = discord.utils.get(member.server.roles, name="verify")
    if ctx.message.channel.name == "verify":
        await bot.add_roles(member, role)
        await bot.say(member.mention + "さんを承認しました。")

@bot.group(pass_context=True)
@commands.has_role("verify")
async def game(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say("`!game <join/leave> <ゲームタイトル>`形式で入力してください。")

@game.command(name='join',pass_context=True)
async def join(ctx, title: str):
    if title in important_roles:
        raise commands.BadArgument()
    else:
        role = discord.utils.get(ctx.message.author.server.roles, name=title)
        await bot.add_roles(ctx.message.author, role)
        await bot.say(ctx.message.author.mention + "さんに{}を追加しました。".format(role))

@game.command(name='leave',pass_context=True)
async def leave(ctx, title: str):
    if title in important_roles:
        raise commands.BadArgument()
    else:
        role = discord.utils.get(ctx.message.author.server.roles, name=title)
        await bot.remove_roles(ctx.message.author, role)
        await bot.say(ctx.message.author.mention + "さんから{}を削除しました。".format(role))

@bot.event
async def on_command_error(exception: Exception, ctx: commands.Context):
        channel = ctx.message.channel
        if isinstance(exception, commands.BadArgument):
            await bot.send_message(channel, "不正な入力です。")
        elif isinstance(exception, commands.CheckFailure):
            await bot.send_message(channel, "コマンドを使う資格がありません。")

bot.run(os.environ["TOKEN"])
