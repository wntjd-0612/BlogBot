import os
import requests
import discord
import schedule
import time

# GitHub API 호출하여 최신 커밋 정보 가져오기
def get_latest_commit(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = requests.get(url)
    if response.status_code == 200:
        commits = response.json()
        if commits:
            latest_commit = commits[0]
            return latest_commit
    return None

# Discord 봇 생성
client = discord.Client()

# 환경 변수에서 Discord 토큰과 채널 ID 가져오기
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

# Discord 봇이 준비되었을 때 실행되는 이벤트 핸들러
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    # GitHub repository 정보
    owner = 'wntjd-0612'
    repo = 'blog'

    # GitHub에서 최신 커밋 정보 가져오기
    latest_commit = get_latest_commit(owner, repo)

    # 최신 커밋 정보를 Discord 채널에 보내기
    if latest_commit:
        message = f"새로운 블로그가 업데이트 되었습니다! 최신 커밋: {latest_commit['sha']}"
        channel = client.get_channel(CHANNEL_ID)
        await channel.send(message)

# Discord 봇 실행
client.run(TOKEN)

# 1분마다 GitHub API를 호출하여 새로운 커밋 확인
schedule.every(1).minutes.do(get_latest_commit, owner, repo)

while True:
    schedule.run_pending()
    time.sleep(1)
