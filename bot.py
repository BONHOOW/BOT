import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio
import datetime
import random
from config import TOKEN, BOT_NAME, BOT_VERSION, BOT_DESCRIPTION, DEVELOPER_ID

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="@", intents=intents)

# 서버 수 추적
server_count = 0

@bot.event
async def on_ready():
    """봇이 준비되었을 때 실행되는 이벤트"""
    print(f"{bot.user} 봇이 성공적으로 로그인했습니다!")
    print(f"봇 이름: {bot.user.name}")
    print(f"봇 ID: {bot.user.id}")
    print(f"서버 수: {len(bot.guilds)}")
    print("=" * 50)
    
    # 서버 수 업데이트
    global server_count
    server_count = len(bot.guilds)
    
    # 상태 메시지 설정
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.custom,
            name="뭘 봐"
        )
    )
    
    # 슬래시 명령어 동기화
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)}개의 슬래시 명령어를 동기화했습니다.")
    except Exception as e:
        print(f"슬래시 명령어 동기화 중 오류: {e}")

@bot.event
async def on_guild_join(guild):
    """봇이 새 서버에 참가했을 때"""
    global server_count
    server_count = len(bot.guilds)
    
    print(f"새 서버에 참가했습니다: {guild.name} (총 {server_count}개 서버)")
    
    # 상태 업데이트
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="뭘 봐"
        )
    )

@bot.event
async def on_guild_remove(guild):
    """봇이 서버에서 제거되었을 때"""
    global server_count
    server_count = len(bot.guilds)
    
    print(f"서버에서 제거되었습니다: {guild.name} (총 {server_count}개 서버)")
    
    # 상태 업데이트
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{server_count}개 서버에서 활성개발자 뱃지 준비 중!"
        )
    )

# 슬래시 명령어들
@bot.tree.command(name="ping", description="봇의 지연시간을 확인합니다")
async def ping(interaction: discord.Interaction):
    """핑 명령어"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"봇 지연시간: **{latency}ms**",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"요청자: {interaction.user.name}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="서버정보", description="현재 서버 정보를 보여줍니다")
async def serverinfo(interaction: discord.Interaction):
    """서버 정보 명령어"""
    guild = interaction.guild
    
    embed = discord.Embed(
        title=f"📊 {guild.name} 서버 정보",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="👑 서버 소유자", value=guild.owner.mention, inline=True)
    embed.add_field(name="👥 멤버 수", value=f"{guild.member_count}명", inline=True)
    embed.add_field(name="📅 생성일", value=guild.created_at.strftime("%Y년 %m월 %d일"), inline=True)
    embed.add_field(name="🎭 역할 수", value=f"{len(guild.roles)}개", inline=True)
    embed.add_field(name="📝 채널 수", value=f"{len(guild.channels)}개", inline=True)
    embed.add_field(name="😀 이모지 수", value=f"{len(guild.emojis)}개", inline=True)
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="봇정보", description="봇 정보를 보여줍니다")
async def botinfo(interaction: discord.Interaction):
    """봇 정보 명령어"""
    embed = discord.Embed(
        title=f"🤖 {BOT_NAME}",
        description=BOT_DESCRIPTION,
        color=discord.Color.purple()
    )
    
    embed.add_field(name="📊 서버 수", value=f"{server_count}개", inline=True)
    embed.add_field(name="👥 총 사용자 수", value=f"{len(bot.users)}명", inline=True)
    embed.add_field(name="⚡ 지연시간", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="🔧 버전", value=BOT_VERSION, inline=True)
    embed.add_field(name="📅 생성일", value=bot.user.created_at.strftime("%Y년 %m월 %d일"), inline=True)
    embed.add_field(name="🆔 봇 ID", value=bot.user.id, inline=True)
    
    embed.set_footer(text="활성개발자 뱃지를 위한 봇입니다!")
    
    if bot.user.avatar:
        embed.set_thumbnail(url=bot.user.avatar.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="활성개발자", description="활성개발자 뱃지 정보를 보여줍니다")
async def active_developer(interaction: discord.Interaction):
    """활성개발자 뱃지 정보"""
    embed = discord.Embed(
        title="🏆 활성개발자 뱃지",
        description="Discord 활성개발자 뱃지를 얻기 위한 조건들입니다!",
        color=discord.Color.gold()
    )
    
    embed.add_field(
        name="📋 필요 조건",
        value="• 봇이 슬래시 명령어를 지원해야 함\n"
              "• 봇이 실제로 사용되고 있어야 함\n"
              "• 봇이 충분한 서버에 초대되어야 함 (정확한 수치는 Discord에서 확인)",
        inline=False
    )
    
    embed.add_field(
        name="📊 현재 상태",
        value=f"• 서버 수: **{server_count}개**\n"
              f"• 슬래시 명령어: ✅ 지원\n"
              f"• 봇 사용: ✅ 활성화",
        inline=False
    )
    
    if server_count >= 75:
        embed.add_field(
            name="🎉 축하합니다!",
            value="충분한 서버에 봇이 초대되었습니다! Discord 개발자 포털에서 활성개발자 뱃지를 확인하세요.",
            inline=False
        )
        embed.color = discord.Color.green()
    elif server_count >= 50:
        embed.add_field(
            name="📈 진행 상황",
            value=f"좋은 진행상황입니다! 현재 {server_count}개 서버에 초대되어 있습니다.",
            inline=False
        )
        embed.color = discord.Color.orange()
    else:
        embed.add_field(
            name="📈 진행 상황",
            value=f"더 많은 서버에 봇을 초대해보세요! 현재 {server_count}개 서버에 초대되어 있습니다.",
            inline=False
        )
    
    embed.set_footer(text="Discord Developer Portal에서 뱃지를 확인하세요!")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="초대링크", description="봇 초대 링크를 생성합니다")
async def invite(interaction: discord.Interaction):
    """봇 초대 링크 생성"""
    invite_url = discord.utils.oauth_url(
        bot.user.id,
        permissions=discord.Permissions(
            send_messages=True,
            read_messages=True,
            use_slash_commands=True,
            embed_links=True,
            attach_files=True
        )
    )
    
    embed = discord.Embed(
        title="🔗 봇 초대 링크",
        description="아래 링크를 클릭하여 봇을 서버에 초대하세요!",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="📋 필요한 권한",
        value="• 메시지 보내기\n"
              "• 메시지 읽기\n"
              "• 슬래시 명령어 사용\n"
              "• 임베드 링크\n"
              "• 파일 첨부",
        inline=False
    )
    
    embed.add_field(
        name="🔗 초대 링크",
        value=f"[봇 초대하기]({invite_url})",
        inline=False
    )
    
    embed.set_footer(text="활성개발자 뱃지 획득을 위해 많은 서버에 초대해주세요!")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="도움말", description="사용 가능한 명령어들을 보여줍니다")
async def help(interaction: discord.Interaction):
    """도움말 명령어"""
    embed = discord.Embed(
        title="📚 명령어 도움말",
        description="사용 가능한 슬래시 명령어들입니다.",
        color=discord.Color.blue()
    )
    
    commands_info = [
        ("🏓 /ping", "봇의 지연시간을 확인합니다"),
        ("📊 /서버정보", "현재 서버 정보를 보여줍니다"),
        ("🤖 /봇정보", "봇 정보를 보여줍니다"),
        ("🏆 /활성개발자", "활성개발자 뱃지 정보를 보여줍니다"),
        ("🔗 /초대링크", "봇 초대 링크를 생성합니다"),
        ("📚 /도움말", "이 도움말을 보여줍니다"),
        ("🎲 /주사위", "1-6 주사위를 굴립니다"),
        ("🎯 /랜덤", "1-100 사이의 랜덤 숫자를 생성합니다"),
        ("⏰ /타이머", "타이머를 설정합니다 (분 단위)"),
        ("📝 /투표", "투표를 생성합니다")
    ]
    
    for cmd, desc in commands_info:
        embed.add_field(name=cmd, value=desc, inline=False)
    
    embed.set_footer(text=f"총 {len(commands_info)}개의 명령어가 있습니다!")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="주사위", description="1-6 주사위를 굴립니다")
async def dice(interaction: discord.Interaction):
    """주사위 명령어"""
    result = random.randint(1, 6)
    embed = discord.Embed(
        title="🎲 주사위",
        description=f"주사위 결과: **{result}**",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"요청자: {interaction.user.name}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="랜덤", description="1-100 사이의 랜덤 숫자를 생성합니다")
async def random_number(interaction: discord.Interaction):
    """랜덤 숫자 생성"""
    result = random.randint(1, 100)
    embed = discord.Embed(
        title="🎯 랜덤 숫자",
        description=f"생성된 숫자: **{result}**",
        color=discord.Color.orange()
    )
    embed.set_footer(text=f"요청자: {interaction.user.name}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="타이머", description="타이머를 설정합니다 (분 단위)")
@app_commands.describe(minutes="타이머 시간 (분)")
async def timer(interaction: discord.Interaction, minutes: int):
    """타이머 명령어"""
    if minutes <= 0 or minutes > 60:
        embed = discord.Embed(
            title="❌ 오류",
            description="타이머 시간은 1-60분 사이여야 합니다.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(
        title="⏰ 타이머 설정",
        description=f"**{minutes}분** 타이머가 설정되었습니다!",
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"요청자: {interaction.user.name}")
    await interaction.response.send_message(embed=embed)
    
    # 타이머 실행
    await asyncio.sleep(minutes * 60)
    
    timer_embed = discord.Embed(
        title="⏰ 타이머 완료!",
        description=f"**{minutes}분** 타이머가 완료되었습니다!",
        color=discord.Color.green()
    )
    timer_embed.set_footer(text=f"요청자: {interaction.user.name}")
    
    try:
        await interaction.followup.send(embed=timer_embed)
    except:
        # 원래 채널에 메시지 보내기
        await interaction.channel.send(content=f"{interaction.user.mention}", embed=timer_embed)

@bot.tree.command(name="투표", description="투표를 생성합니다")
@app_commands.describe(question="투표 질문", option1="옵션 1", option2="옵션 2")
async def poll(interaction: discord.Interaction, question: str, option1: str, option2: str):
    """투표 생성 명령어"""
    embed = discord.Embed(
        title="📝 투표",
        description=f"**{question}**",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="1️⃣", value=option1, inline=True)
    embed.add_field(name="2️⃣", value=option2, inline=True)
    
    embed.set_footer(text=f"투표 생성자: {interaction.user.name}")
    
    message = await interaction.response.send_message(embed=embed)
    
    # 반응 추가
    try:
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
    except:
        pass

# Prefix 명령어들 (@로 시작하는 명령어)
@bot.command(name="ping")
async def prefix_ping(ctx):
    """Prefix 핑 명령어"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"봇 지연시간: **{latency}ms**",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"요청자: {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command(name="도움말")
async def prefix_help(ctx):
    """Prefix 도움말 명령어"""
    embed = discord.Embed(
        title="📚 명령어 도움말",
        description="사용 가능한 명령어들입니다.",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🔧 Prefix 명령어 (@로 시작)",
        value="• `@ping` - 봇의 지연시간 확인\n"
              "• `@도움말` - 이 도움말 보기\n"
              "• `@서버정보` - 서버 정보 확인\n"
              "• `@봇정보` - 봇 정보 확인\n"
              "• `@활성개발자` - 뱃지 정보 확인",
        inline=False
    )
    
    embed.add_field(
        name="⚡ 슬래시 명령어 (/로 시작)",
        value="• `/ping` - 봇의 지연시간 확인\n"
              "• `/서버정보` - 서버 정보 확인\n"
              "• `/봇정보` - 봇 정보 확인\n"
              "• `/활성개발자` - 뱃지 정보 확인\n"
              "• `/초대링크` - 봇 초대 링크\n"
              "• `/도움말` - 명령어 목록\n"
              "• `/주사위` - 주사위 굴리기\n"
              "• `/랜덤` - 랜덤 숫자\n"
              "• `/타이머` - 타이머 설정\n"
              "• `/투표` - 투표 생성",
        inline=False
    )
    
    embed.set_footer(text="Prefix 명령어는 @로, 슬래시 명령어는 /로 시작합니다!")
    await ctx.send(embed=embed)

@bot.command(name="서버정보")
async def prefix_serverinfo(ctx):
    """Prefix 서버 정보 명령어"""
    guild = ctx.guild
    
    embed = discord.Embed(
        title=f"📊 {guild.name} 서버 정보",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="👑 서버 소유자", value=guild.owner.mention, inline=True)
    embed.add_field(name="👥 멤버 수", value=f"{guild.member_count}명", inline=True)
    embed.add_field(name="📅 생성일", value=guild.created_at.strftime("%Y년 %m월 %d일"), inline=True)
    embed.add_field(name="🎭 역할 수", value=f"{len(guild.roles)}개", inline=True)
    embed.add_field(name="📝 채널 수", value=f"{len(guild.channels)}개", inline=True)
    embed.add_field(name="😀 이모지 수", value=f"{len(guild.emojis)}개", inline=True)
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    await ctx.send(embed=embed)

@bot.command(name="봇정보")
async def prefix_botinfo(ctx):
    """Prefix 봇 정보 명령어"""
    embed = discord.Embed(
        title=f"🤖 {BOT_NAME}",
        description=BOT_DESCRIPTION,
        color=discord.Color.purple()
    )
    
    embed.add_field(name="📊 서버 수", value=f"{server_count}개", inline=True)
    embed.add_field(name="👥 총 사용자 수", value=f"{len(bot.users)}명", inline=True)
    embed.add_field(name="⚡ 지연시간", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="🔧 버전", value=BOT_VERSION, inline=True)
    embed.add_field(name="📅 생성일", value=bot.user.created_at.strftime("%Y년 %m월 %d일"), inline=True)
    embed.add_field(name="🆔 봇 ID", value=bot.user.id, inline=True)
    
    embed.set_footer(text="활성개발자 뱃지를 위한 봇입니다!")
    
    if bot.user.avatar:
        embed.set_thumbnail(url=bot.user.avatar.url)
    
    await ctx.send(embed=embed)

@bot.command(name="활성개발자")
async def prefix_active_developer(ctx):
    """Prefix 활성개발자 뱃지 정보"""
    embed = discord.Embed(
        title="🏆 활성개발자 뱃지",
        description="Discord 활성개발자 뱃지를 얻기 위한 조건들입니다!",
        color=discord.Color.gold()
    )
    
    embed.add_field(
        name="📋 필요 조건",
        value="• 봇이 슬래시 명령어를 지원해야 함\n"
              "• 봇이 실제로 사용되고 있어야 함\n"
              "• 봇이 충분한 서버에 초대되어야 함 (정확한 수치는 Discord에서 확인)",
        inline=False
    )
    
    embed.add_field(
        name="📊 현재 상태",
        value=f"• 서버 수: **{server_count}개**\n"
              f"• 슬래시 명령어: ✅ 지원\n"
              f"• 봇 사용: ✅ 활성화",
        inline=False
    )
    
    if server_count >= 75:
        embed.add_field(
            name="🎉 축하합니다!",
            value="충분한 서버에 봇이 초대되었습니다! Discord 개발자 포털에서 활성개발자 뱃지를 확인하세요.",
            inline=False
        )
        embed.color = discord.Color.green()
    elif server_count >= 50:
        embed.add_field(
            name="📈 진행 상황",
            value=f"좋은 진행상황입니다! 현재 {server_count}개 서버에 초대되어 있습니다.",
            inline=False
        )
        embed.color = discord.Color.orange()
    else:
        embed.add_field(
            name="📈 진행 상황",
            value=f"더 많은 서버에 봇을 초대해보세요! 현재 {server_count}개 서버에 초대되어 있습니다.",
            inline=False
        )
    
    embed.set_footer(text="Discord Developer Portal에서 뱃지를 확인하세요!")
    await ctx.send(embed=embed)

# 에러 핸들링
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """슬래시 명령어 에러 처리"""
    print(f"명령어 에러 발생: {error}")
    
    try:
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = discord.Embed(
                title="⏳ 쿨다운",
                description=f"이 명령어는 {error.retry_after:.2f}초 후에 다시 사용할 수 있습니다.",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="❌ 오류 발생",
                description=f"명령어 실행 중 오류가 발생했습니다: {str(error)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        print(f"에러 처리 중 추가 오류: {e}")
        try:
            await interaction.response.send_message("명령어 실행 중 오류가 발생했습니다.", ephemeral=True)
        except:
            pass

# 봇 실행
if __name__ == "__main__":
    print(f"{BOT_NAME} v{BOT_VERSION} 시작 중...")
    print("=" * 50)
    bot.run(TOKEN)
