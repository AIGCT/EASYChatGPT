from revChatGPT.Official import Chatbot

from config import getToken

openai_key = getToken()

# 初始化bot
chatbot = Chatbot(api_key=openai_key)


def run():

    # 打印蓝色字迹的输出
    print("\033[1;33m" +
          "遇到报错优先考虑重新运行" + "\033[0m \n")
    input_text = ""

    while input_text != "quit":

        # 打印蓝色字迹的输出
        print("\033[1;34m" + "你的 输入: " + "\033[0m")
        input_text = input()

        out = chatbot.ask(input_text)
        # 打印绿色字迹的输出
        print("\033[1;32m" + "ChatGPT 输出: " + "\033[0m")
        # 打印输出
        print(out["choices"][0]["text"])
        # 黄色分割线
        print("\033[1;33m" +
              "-----------------------------------------" + "\033[0m")


if __name__ == "__main__":
    run()
