from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from utils.database import UserDB
import functions as f
import slack_sdk
import os
import textwrap

load_dotenv()
BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
APP_TOKEN = os.getenv('SLACK_APP_TOKEN')
SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')

db = UserDB()

STATE_WAITING_FIRST = 'waiting_first_input'
STATE_WAITING_SECOND = 'waiting_second_input'
STATE_COMPLETE = 'complete'
STATE_WAITING_CHANGE = 'waiting_nickname_change'
# STATE_INVITING_FRIEND = 'wating_invite'

app = App(token=BOT_TOKEN, signing_secret=SIGNING_SECRET)

@app.command('/가입')
def register(ack, command, client):
    ack()
    user_id = command['user_id']
    response = client.users_info(user=user_id)
    slack_name = response['user']['profile']['display_name']
    if not slack_name:
        slack_name = response['user']['name']

    db.save_user_state(user_id, STATE_WAITING_FIRST)
    db.save_slack_name(user_id, slack_name)

    conversations_response = app.client.conversations_open(users=user_id)
    channel_id = conversations_response['channel']['id']

    app.client.chat_postMessage(
        channel = channel_id,
        text = textwrap.dedent("""
            *--------------------------------------------------------------------------------*\n
            💚환영합니다💚\n\n\
            아그작은 백준 온라인 저지를 통해 진행됩니다!\n\
            따라서 백준 아이디가 없으신 경우 가입 부탁드립니다👍\n\n\
            BOJ 아이디를 채팅에 적어주세요!!\n
            *--------------------------------------------------------------------------------*\n
        """)
    )

@app.command('/닉변')
def change_nickname(ack, command):
    ack()
    user_id = command['user_id']

    db.save_user_state(user_id, STATE_WAITING_CHANGE)

    conversations_response = app.client.conversations_open(users=user_id)
    channel_id = conversations_response['channel']['id']

    app.client.chat_postMessage(
        channel = channel_id,
        text = textwrap.dedent("""
            *--------------------------------------------------------------------------------*\n
            변경하실 닉네임을 채팅에 적어주세요!
            *--------------------------------------------------------------------------------*\n
        """)
    )

# @app.command('/친구초대')
# def invite_friend(ack, command):
#     ack()
#     user_id = command['user_id']

#     db.save_user_state(user_id, STATE_INVITING_FRIEND)

#     conversations_response = app.client.conversations_open(users=user_id)
#     channel_id = conversations_response['channel']['id']

#     app.client.chat_postMessage(
#         channel = channel_id,
#         text = textwrap.dedent("""
#             *--------------------------------------------------------------------------------*\n
#             초대하실 친구의 백준 아이디를 입력해주세요!
#             *--------------------------------------------------------------------------------*\n
#         """)
#     )

@app.message('')
def user_input(message, say, client):
    channel_info = client.conversations_info(channel=message['channel'])
    
    if not channel_info['channel']['is_im']:
        return
    
    user_id = message['user']
    user_text = message['text']
    
    current_state = db.get_user_state(user_id)
    
    if current_state is None:
        say("먼저 '/가입' 명령어를 입력해주세요.")
        return
    
    if current_state == STATE_WAITING_FIRST:
        if not f.check_id(user_text):
            say(textwrap.dedent("""
                *--------------------------------------------------------------------------------*\n
                존재하지 않는 아이디 입니다. 다시 입력해주세요!
                *--------------------------------------------------------------------------------*\n
            """))
            return
        
        elif f.dup_id(user_text):
            say(textwrap.dedent("""
                *--------------------------------------------------------------------------------*\n
                이미 가입이 완료된 아이디 입니다.\n\n
                아그작 탈퇴를 원하시면 '/탈퇴'를,\n
                닉네임 변경을 원하시면 '/닉변'을 입력해주세요!\n
                *--------------------------------------------------------------------------------*\n
            """))
            db.save_user_state(user_id, None)
            return
        
        db.save_user_info(user_id, BOJ_id=user_text)
        db.save_user_state(user_id, STATE_WAITING_SECOND)
        
        say(textwrap.dedent(f"""
            *--------------------------------------------------------------------------------*\n
            {user_text}님 반갑습니다!! 정말 멋진 아이디네요😊\n
            다음으로는 본인만의 닉네임을 작성해 주세요. 예) zi존 아이그루스\n
            *--------------------------------------------------------------------------------*\n
        """))
    
    elif current_state == STATE_WAITING_SECOND:
        if f.dup_name(user_id, user_text):
            say(textwrap.dedent("""
                *--------------------------------------------------------------------------------*\n
                존재하는 닉네임 입니다. 다시 입력해주세요.
                *--------------------------------------------------------------------------------*\n
            """))
            return

        db.save_user_info(user_id, user_name=user_text)
        db.save_user_state(user_id, STATE_COMPLETE)
        
        user_info = db.get_user_info(user_id)
        
        say(textwrap.dedent(f"""
            *--------------------------------------------------------------------------------*\n
            아그작 가입이 완료되었습니다! 🎉\n\n\
            *유저 정보:*\n\
            • 백준 ID: {user_info['BOJ_id']}\n\
            • 닉네임: {user_info['user_name']}\n\n\
            *필독!!*\n
            아그작은 백준 그룹을 통해서 진행 됩니다.\n
            문제는 매주 월요일 공지 및 백준 그룹의 연습 탭에서 확인하실 수 있습니다.\n\n
            *주의사항!!*\n
            그룹에 초대되기 전에 문제를 해결하면 스코어보드에 집계가 안 됩니다!\n
            이 경우에는 그룹에 초대되신 후 문제를 재제출하시면 됩니다.
            *--------------------------------------------------------------------------------*\n
        """))
    
    elif current_state == STATE_WAITING_CHANGE:
        stat = f.same_name(user_id, user_text)
        if stat == 'same':
            say(textwrap.dedent("""
                *--------------------------------------------------------------------------------*\n
                이전과 동일한 닉네임 입니다. 다시 입력해주세요.
                *--------------------------------------------------------------------------------*\n
            """))
            return
        elif stat == 'duplicate':
            say(textwrap.dedent("""
                *--------------------------------------------------------------------------------*\n
                존재하는 닉네임 입니다. 다시 입력해주세요.
                *--------------------------------------------------------------------------------*\n
            """))
            return
        elif stat == 'complete':
            user_info = db.get_user_info(user_id)

            say(textwrap.dedent(f"""
                *--------------------------------------------------------------------------------*\n
                닉네임 변경이 완료 되었습니다!\n
                • 기존 닉네임: {user_info['user_name']}\n
                • 변경후 닉네임: {user_text}
                *--------------------------------------------------------------------------------*\n
            """))

            db.save_user_info(user_id, user_name=user_text)
    # elif current_state == STATE_INVITING_FRIEND:
        
    elif current_state == STATE_COMPLETE:
        say("이미 입력이 완료되었습니다. 새로운 입력을 원하시면 '/가입' 명령어를 입력해주세요.")

@app.command('/탈퇴')
def withdraw(ack, command):
    ack()
    user_id = command['user_id']

    conversations_response = app.client.conversations_open(users=user_id)
    channel_id = conversations_response['channel']['id']

    app.client.chat_postMessage(
        channel = channel_id,
        text = textwrap.dedent("""
            *--------------------------------------------------------------------------------*\n
            아그작 탈퇴가 완료되었습니다!\n
            *--------------------------------------------------------------------------------*\n
        """)
    )

    db.clear_user_data(user_id)
    
if __name__=='__main__':
    handler = SocketModeHandler(app, APP_TOKEN)
    handler.start()