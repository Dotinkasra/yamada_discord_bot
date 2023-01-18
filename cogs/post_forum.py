from discord.ext import commands
from discord import app_commands
import discord

class PostForum(commands.Cog):
    """
    PostForumクラスは、discordのサーバーにおいて、特定のフォーラムに投稿するCogです

    Parameters
    ----------
    commands : commands.Bot
        Botのインスタンス
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        botが起動した時に実行され、Cogの読み込みが完了したことを示すメッセージを出力します。
        """
        print('Successfully loaded : PostForum')

    @app_commands.command(name = "postforum", description = "*管理者限定 forumに投稿")
    @app_commands.choices(select_forum = [
        app_commands.Choice(name = "通常", value = "1060959454243336343"),
        app_commands.Choice(name = "R18", value = "1060963546600587436"),
    ])
    @app_commands.choices(select_tags = [
        app_commands.Choice(name = "つぶやき", value = "つぶやき"),
        app_commands.Choice(name = "画像", value = "画像"),
        app_commands.Choice(name = "動画", value = "動画"),
    ])
    @app_commands.describe(title = "投稿するフォーラムのタイトルです。")
    @app_commands.describe(msg = "投稿するフォーラムの本文です。")
    @app_commands.describe(select_forum = "投稿先のフォーラムを指定してください。")
    @app_commands.describe(select_tags = "フォーラムに付与するタグを選択してください。")
    @app_commands.guilds(1054929219144130703)
    @app_commands.checks.has_permissions(administrator=True)
    async def postforum(
        self, interaction: discord.Interaction,
        title: str,
        msg: str,
        select_forum: app_commands.Choice[str],
        select_tags: app_commands.Choice[str],
        file_name: str = None,
    ) -> None:
        """
        フォーラム投稿用のメソッド

        Parameters
        ----------
        interaction : discord.Interaction
            受け取ったInteraction
        title : str
            フォーラムのタイトル
        msg : str
            フォーラムの本文
        select_forum : app_commands.Choice[str]
            投稿先
        select_tags : app_commands.Choice[str]
            投稿するフォーラムに付与するタグ
        file_name : str, optional
            ファイルが有る場合は、ファイル名を指定する default: None
        """
        channel = interaction.guild.get_channel(int(select_forum.value))
        
        tag = None

        # R18 には 「つぶやき」　が存在せず　相当するタグに　「メモ」　があるので　そちらに変更
        if select_forum.name == "R18" and select_tags.value == "つぶやき":
            tag = list(filter(lambda x: x.name == "メモ", channel.available_tags))
        else:
            tag = list(filter(lambda x: x.name == select_tags.value, channel.available_tags)) 
        print(tag)
        print(channel)

        if file_name:
            await channel.create_thread(
                    name = title,
                    content = msg,
                    applied_tags = tag,
                    file = discord.File(file_name)
                )
        else:
            await channel.create_thread(
                    name = title,
                    content = msg,
                    applied_tags = tag,
                )

        await interaction.response.send_message("test", ephemeral=True)
            
async def setup(bot: commands.Bot):
    await bot.add_cog(PostForum(bot))
