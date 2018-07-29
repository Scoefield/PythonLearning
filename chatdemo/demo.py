import itchat

# login wechat
# itchat.login()
itchat.auto_login(hotReload=True)

friends = itchat.get_friends()[0:]
# print(friends)

male = 0
female = 0
other = 0

for i in friends[1:]:
    sex = i['Sex']
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
        other += 1
    
total = len(friends[1:])
print("The man: %.2f%%" % float(male/total*100))
print("The women: %.2f%%" % float(female/total*100))