from discord.ext import commands, tasks
import discord

class CallCounter(commands.Cog):
    """
    CallCounterクラスは、Discordのサーバーにおける通話中の人数を数え上げ、それを表示するクラスです。
    また、参加人数の多い声チャンネルの上位2つをランキング形式で表示します。

    Parameters
    ----------
    bot: commands.Bot
        Botのインスタンス
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ranking_one: discord.VoiceChannel | None = None
        self.ranking_two: discord.VoiceChannel | None = None

    def __set_server_info(self):
        """
        必要なサーバー情報を設定します。
        """
        my_server_id = 1054929219144130703
        notification_channel = 1060633792655671467
        notification_category = 1060633672895709295

        self.guild: discord.Guild | None = self.bot.get_guild(my_server_id)
        self.target: discord.abc.GuildChannel | None = self.guild.get_channel(notification_channel)
        self.category: tuple[
                discord.CategoryChannel | None,
                list[discord.abc.GuildChannel]
            ] = list(filter(lambda x: x[0].id == notification_category, self.guild.by_category()))[0]

    def __sum_voicechannel_members(self, voicechannels: list[discord.VoiceChannel]) -> int:
        """
        引数で渡された声チャンネルに接続しているメンバー数を合計します

        Parameters
        ----------
        voicechannels: list[discord.VoiceChannel]
            合計を求める声チャンネルのリスト

        Returns
        -------
        int
            合計人数
        """
        return sum(len([m for m in vc.members if not m.bot]) for vc in voicechannels)

    def __order_by_participants(self) -> list[discord.VoiceChannel]:
        """
        参加人数の多い順に声チャンネルをソートします

        Returns
        -------
        list[discord.VoiceChannel]
            参加人数の降順にソートされた声チャンネルのリスト
        """
        no_count_channel_ids: list[int] = [
            1058321624203530290,
        ]
        channels = [channel for channel in self.guild.voice_channels if channel.id not in no_count_channel_ids]
        return sorted(channels, key=lambda x: len(x.members), reverse=True)

    def __get_not_access_permissions(self) -> dict:
        """
        接続権限がない権限設定を返します

        Returns
        -------
        dict
            接続権限がない権限設定
        """
        return { self.guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=True) }

    def __get_counters_channel_name(self, count) -> str:
        """
        カウンターチャンネルの名前を返します

        Parameters
        ----------
        count : int
            カウント数

        Returns
        -------
        str
            カウンターチャンネルの名前
        """
        party_boarder = 7
        if count > party_boarder:
            return str("🟡￤大盛況:{}人".format(str(count)))
        if count:
            return str("🟢￤通話中:{}人".format(str(count)))
        return str("🔴￤通話してません")

    async def __switch_counters(self, count: int) -> None:
        """
        カウンターチャンネルの名前を変更します

        Parameters
        ----------
        count : int
            カウント数
        """
        print(count)
        await self.target.edit(name = self.__get_counters_channel_name(count))

    async def __find_rank1(self, count: int, voicechannels: list[discord.VoiceChannel]) -> None:
        """
        ランキング1位の処理を行います

        Parameters
        ----------
        count : int
            カウント数
        voicechannels : list[discord.VoiceChannel]
            参加人数の降順にソートされた声チャンネルのリスト
        """
        if count and len(voicechannels[0].members):
            name = f"🥇￤{voicechannels[0].name}:{str(len(voicechannels[0].members))}"
            if self.ranking_one is None:
                self.ranking_one = await self.category[0].create_voice_channel(
                    name,
                    overwrites = self.__get_not_access_permissions(),
                )
            else:
                await self.ranking_one.edit(
                    name = name,
                )

        elif count == 0 and self.ranking_one is not None:
            await self.ranking_one.delete()
            self.ranking_one = None


    async def __find_rank2(self, count: int, voicechannels: list[discord.VoiceChannel]) -> None:
        """
        ランキング2位の処理を行います

        Parameters
        ----------
        count : int
            カウント数
        voicechannels : list[discord.VoiceChannel]
            参加人数の降順にソートされた声チャンネルのリスト
        """
        if count and len(voicechannels[1].members):
            name = f"🥈￤{voicechannels[1].name}:{str(len(voicechannels[1].members))}"
            if self.ranking_two is None:
                self.ranking_two = await self.category[0].create_voice_channel(
                    name,
                    overwrites = self.__get_not_access_permissions(),
                )
            else:
                await self.ranking_two.edit(
                    name = name,
                )

        elif count == 0 and self.ranking_two is not None:
            await self.ranking_two.delete()
            self.ranking_two = None


    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : CallCounter')
        if not self.count.is_running():
            self.count.start()

    @tasks.loop(seconds=300)
    async def count(self):
        print("実行")
        self.__set_server_info()

        vc_list = self.__order_by_participants()
        count = self.__sum_voicechannel_members(vc_list)

        await self.__switch_counters(count)
        #await self.__find_rank1(count, vc_list)
        #await self.__find_rank2(count, vc_list)
                
            
def setup(bot):
    return bot.add_cog(CallCounter(bot))