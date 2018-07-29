import itchat

itchat.auto_login(hotReload=True)

friends = itchat.get_friends()[0:]

friend_dict = {}
for friend in friends:
    signature = friend['Signature']
    friend_dict[friend['RemarkName']] = signature
    # print(friend_dict)
    # print(type(signature), signature)

path = "/home/dys/pythonTest/chatdemo/signature.txt"
with open(path, 'a') as f:
    for key, value in friend_dict.items():
        if value and len(value)>2:
            # f.write(key + ':' + value + '\n')
            f.write(value + '\n')

itchat.run()