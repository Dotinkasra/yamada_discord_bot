from discord.ext import commands
from discord import app_commands
import discord

class SendDM(commands.Cog):
    """
    BANした後にDMを送るコマンド

    Parameters
    ----------
    commands : commands.Bot
        Botのインスタンス
    """
    def __init__(self, bot: commands.Cog):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : PostForum')

    @app_commands.command(name = "ban", description = "*管理者限定 人をBANします")
    @app_commands.describe(member= "BANしたいメンバー")
    @app_commands.guilds(1054929219144130703)
    @app_commands.checks.has_permissions(administrator=True)
    async def postforum(
        self, interaction: discord.Interaction,
        member: discord.Member = None,
        user_id: str = None,
    ) -> None:
        """
        BANし、DMを送信するメソッド

        Parameters
        ----------
        interaction : discord.Interaction
            受け取ったinteraction
        member : discord.Member
            BAN対象のメンバー
        user_id : str
            BAN対象のユーザーID, memberかuser_idのどちらかを指定しなければならない
        """
        if member is None and user_id is None:
            return
        if member is None and user_id is not None:
            try:
                member = await self.bot.fetch_user(int(user_id))
            except Exception as e:
                print(e)
        s = """
        F = (Σm(x ∈ S) / Σ(g + m)(x ∈ A)) - T_r(U) / (1 - T_r(U))

        F: 迷惑行為係数
        m: あなたの迷惑行為
        S: 全サーバー
        g: あなたの善行
        A: あなたの全ての行動
        T_r(U) : サーバー参加者の迷惑許容度の割合
        U: サーバー参加者

        上記の式は、全サーバーでの迷惑行為の総数、対象の行動における全ての行動の総数、システムユーザーの迷惑許容度を使用して、
        そのユーザーが将来どの程度迷惑行為をする可能性が高いかを数値化した迷惑行為係数を求めるものです。
        """
        embed = discord.Embed(
            title="山田皓型心理診断チンポコ執行システム",
            color=0x00ff00,
        )
        embed.add_field(name="執行対象", value="{}".format(member.name), inline=True)
        embed.add_field(name="迷惑係数", value="オーバー300", inline=True)
        embed.add_field(name="詳細", value=s, inline=False)
        #embed.set_footer(text="全ての詳細は ドラカス#5334 または まんぽ#6972 に問い合わせてください。")
        await member.send(embed=embed)
        await interaction.response.send_message("BANned {}".format(member), ephemeral=True)
        await member.ban(reason="山田皓型心理診断チンポコ執行システムにより")
            
async def setup(bot: commands.Bot):
    await bot.add_cog(SendDM(bot))

