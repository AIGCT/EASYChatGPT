from revChatGPT.revChatGPT import Chatbot
import time
import random
# from config import getToken

# config = getToken()

user_session = dict()
# 初始化bot
chatbot = Chatbot({})

# 刷新seesion_token
chatbot.refresh_session()


def get_chat_response(session_id, prompt):

    if session_id in user_session:
        # 如果在10分钟内再次发起对话则使用相同的会话ID
        if time.time() < user_session[session_id]['timestamp'] + 60 * 10:
            chatbot.conversation_id = user_session[session_id]['conversation_id']
            chatbot.parent_id = user_session[session_id]['parent_id']
        else:
            chatbot.reset_chat()
    else:
        chatbot.reset_chat()
    try:
        resp = chatbot.get_chat_response(prompt, output="text")
        user_cache = dict()
        user_cache['timestamp'] = time.time()
        user_cache['conversation_id'] = resp['conversation_id']
        user_cache['parent_id'] = resp['parent_id']
        user_session[session_id] = user_cache
        return resp['message']
    except Exception as e:
        print(e)
        return f"发生错误: {str(e)}"


def run():

    # 打印蓝色字迹的输出
    print("\033[1;33m" +
          "遇到报错优先考虑重新运行,程序内置了很多token,随机选择一个使用，所以多次运行即可" + "\033[0m \n")
    input_text = ""
    random_session_id = str(random.randint(100, 99999))
    while input_text != "quit":

        # 打印蓝色字迹的输出
        print("\033[1;34m" + "你的 输入: " + "\033[0m")
        input_text = input()

        out = get_chat_response(random_session_id, input_text)
        # 打印绿色字迹的输出
        print("\033[1;32m" + "ChatGPT 输出: " + "\033[0m")
        # 打印输出
        print(out)
        # 黄色分割线
        print("\033[1;33m" +
              "-----------------------------------------" + "\033[0m")


if __name__ == "__main__":
    run()
