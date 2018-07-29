import itchat

itchat.auto_login(hotReload=True)

friends = itchat.get_friends()[0:]

for friend in friends:
    img = itchat.get_head_img(userName=friend['UserName'])
    # print(friend)
    # exit()
    path = "/home/dys/pythonTest/chatdemo/img/" + friend['RemarkName'] + '.jpg'
    # print(path)
    print("Loading the %s head_img" % friend['RemarkName'])
    try:
        with open(path, 'wb') as f:
            f.write(img)
    except Exception as e:
        print("Write fail:", e)

itchat.run()