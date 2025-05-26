import os
import time
from llm_ollama import GPT_OLLAMA
from wxauto import WeChat

robot = GPT_OLLAMA()

wx = WeChat()
# 指定监听目标
listen_list = [
    '范元琛',
    '何军军',
    '🌾麦田守望者',
    '拓客云',
    '科技部',
    '熊敏杰',
    '李炳洪',
    '王霓',
    '杨嘉文',
    '哈哈',
    '庞浩',
    '叶小丽',
    '陈思佳-网金',
    '姚文琳',
    '麦晓飞',
    '三个臭皮匠🙏🏻🥹'

]
for friend in listen_list:
    print("开始监听好友："+friend)
    wx.AddListenChat(who=friend)  # 添加监听对象
    

# 持续监听消息，有消息则对接大模型进行回复
wait = 1  # 设置1秒查看一次是否有新消息
while True:
    msgs = wx.GetListenMessage()
    for chat in msgs:
        msg = msgs.get(chat)   # 获取消息内容
        for i in msg:
            
            if i.type == 'friend':
                at_me = "@"+wx.nickname
                print("收到好友消息："+i.content+"---"+at_me)
                reply = robot.talk(i.content)
                #chat.SendMsg("qwen3:32b:"+reply)  # 回复
            else:
                print("收到未知类型："+ i.type+"->"+i.content)
    time.sleep(wait)