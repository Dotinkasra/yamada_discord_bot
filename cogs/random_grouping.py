from discord.ext import commands
from discord import app_commands
import discord
import random
import asyncio

class randomGrouping(commands.Cog):
    """
    discordのサーバーにおいて、グループ分けを行うCogです。

    Parameters
    ----------
    commands : commands.Bot
        Botのインスタンス
    """
    def __init__(self, bot: commands.Cog):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        botが起動した時に実行され、Cogの読み込みが完了したことを示すメッセージを出力します。
        """
        print('Successfully loaded : randomGrouping')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if not reaction.message.id == self.start_msg.id:
            return
        text = await self.get_reaction_members([reaction])
        await self.results_msg.delete()
        if text:
            self.results_msg = await reaction.message.channel.send(embed= text)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        print(reaction.message.id, self.start_msg.id)
        print(reaction)
        if not reaction.message.id == self.start_msg.id:
            return
        text = await self.get_reaction_members([reaction])
        await self.results_msg.delete()
        if text:
            self.results_msg = await reaction.message.channel.send(embed= text)

    @app_commands.command(name = "grouping", description = "グループ分けします")
    @app_commands.describe(num_of_groups= "グループの数")
    @app_commands.guilds(1054929219144130703)
    @app_commands.checks.has_permissions(administrator=True)
    async def grouping(
        self, interaction: discord.Interaction,
        num_of_groups: int = 2,
    ) -> None:
        """
        グループ分けを行うコマンドです。

        Parameters
        ----------
        interaction: discord.Interaction
            discordのInteractionオブジェクト。
        num_of_groups: int, optional
            グループ数。デフォルトは2
        """
        self.start_msg = await interaction.channel.send("10秒間の投票を行います。")
        self.num_of_groups = num_of_groups

        #10秒間の投票を行う
        await self.start_msg.add_reaction("✅")
        await asyncio.sleep(10)

        #リアクションが付き終わってから、もう一度メッセージを取得
        reload_start_msg = await interaction.channel.fetch_message(self.start_msg.id)
        text = await self.get_reaction_members(reload_start_msg.reactions)
        if text:
            #グループ分けの結果を送信
            self.results_msg = await interaction.channel.send(embed=text)

    async def get_reaction_members(self, reactions: list[discord.Reaction]) -> discord.Embed | None:
        all_reaction_members = []        
        for reaction in reactions:
            #反応した人のリストを取得（botを除く）
            all_reaction_members.append([m async for m in reaction.users() if not m.bot])
            
        all_reaction_members = list(
            set(
                member for one_reaction_members in all_reaction_members for member in one_reaction_members
            )
        )

        #グループ分けをする
        result_group = self.do_random_grouping(all_reaction_members, self.num_of_groups)
        if len(result_group) == 0:
            return None
        
        embed = discord.Embed(title="チーム分け結果", description="以下の通りです。", color=0x8f70ff)

        for i, group in enumerate(result_group):
            group_name = "チーム" + chr(ord("A") + i)
            embed.add_field(name = group_name, value = ", ".join([m.name for m in group]), inline=False)
            
        return embed
    
    def do_random_grouping(self, members: list, number_of_groups: int) -> list:
        """
        グループ分けを行う関数です。

        Parameters
        ----------
        members : list
            グループ分けを行うメンバーのリスト。
        number_of_groups : int
            グループ数。
        
        Returns
        -------
        list
            グループ分け後のリスト。
        """
        if number_of_groups == 0:
            return []

        #メンバーをランダムに並べ替え
        random.shuffle(members)
        groups = [[] for _ in range(number_of_groups)]
        for i, member in enumerate(members):
            #グループ数で割った余りをインデックスに利用して、グループに追加
            groups[i%number_of_groups].append(member)
        return list(filter(None, groups))

async def setup(bot: commands.Bot):
    await bot.add_cog(randomGrouping(bot))
