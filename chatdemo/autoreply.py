import itchat
import requests

itchat.auto_login(hotReload=True)

apiUrl = "http://www.tuling123.com/openapi/api"

def get_info(message):
    data = {
        'key': 'b30d28f5ec2c46e4a7ea35c2f7f3445e',
        'info': message,
        'userid': 'robot'
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        info = r['text']
        print("Robot replay: %s" % info)
        return info
    except:
        pass

# get_info("你好")

@itchat.msg_register(itchat.content.TEXT)
def auto_reply(msg):
    # defaultReply = "I know"
    realFriend = itchat.search_friends(name='不会放电的皮卡丘')
    # print(realFriend)
    realFriendName = realFriend[0]['UserName']
    # print(realFriendName)

    # print friend reply msg
    print("Friend message: %s " % msg['Text'])
    reply = get_info(msg['Text'])
    # print(reply)
    if msg['FromUserName'] == realFriendName:
        itchat.send(reply, toUserName=realFriendName)

itchat.run()
# auto_reply("hello")
