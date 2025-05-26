import os
import time
from llm_ollama import GPT_OLLAMA
from wxauto import WeChat

robot = GPT_OLLAMA()

wx = WeChat()
# 指定监听目标
listen_list = [
    '拓客云',
    '科技部',
    '悦享民生小程序',
    '哈哈',
    '三个臭皮匠🙏🏻🥹',
    '范元琛',
    '何军军',
    '🌾麦田守望者',
    '熊敏杰',
    '李炳洪',
    '王霓',
    '竹米',
    '杨嘉文',
    '庞浩',
    '叶小丽',
    '陈思佳-网金',
    '姚文琳',
    '麦晓飞',
]
# 定义自己的群名称
group_dict ={
    "哈哈":"开心",
    "拓客云":"张少举",
    "悦享民生小程序":"张少举",
    "三个臭皮匠🙏🏻🥹":"张少举"
    
}
for friend in listen_list:
    print("开始监听好友："+friend)
    wx.AddListenChat(who=friend)  # 添加监听对象

# 持续监听消息，有消息则对接大模型进行回复
wait = 1  # 设置1秒查看一次是否有新消息
while True:
    chats = wx.GetListenMessage()   # 获取监听的所有聊天窗口
    for chat in chats:
        chat_title = chat.who       #当前聊天窗口
        msgs = chats.get(chat)   # 获取当前聊天窗口的信息
        for one_msg in msgs:
            sender = one_msg.info[0]    #发送消息的人
            if one_msg.type == 'friend':
                # 判断消息来自群组还是个人
                # 个人直接回复
                # 群组需检测是否是@自己的消息
                if chat_title == sender:
                    print("消息来自个人:"+chat_title)
                    reply = robot.talk(one_msg.content)
                    chat.SendMsg(reply)
                else:
                    print("消息来自群："+chat_title+" 中的："+sender)
                    at_me = "@"+ group_dict.get(chat_title) if group_dict.get(chat_title) is not None else wx.nickname
                    if at_me in one_msg.content:
                        real_msg = one_msg.content.replace(at_me,"")
                        reply = robot.talk(real_msg)
                        #chat.SendMsg("@"+sender+" "+reply) # 拼接出来的起不到@的效果，没有提醒
                        wx.SendMsg(msg=reply, who=chat_title, at=sender)    # 可以实现@,但是emoji表情的昵称会出问题
                    else:
                        print("忽略群消息："+one_msg.content)
            elif one_msg.type == 'self':
                print("收到来自自己的消息："+one_msg.content)
            else:
                print("收到未知类型："+ one_msg.type+"->"+one_msg.content)
    time.sleep(wait)