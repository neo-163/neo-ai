from openai import OpenAI

# 设置 OpenAI 客户端
openai_client = OpenAI(base_url="http://127.0.0.1:8100/v1", api_key="not-needed")

# 对话历史：设定系统角色是一个智能助理
history = [
    {"role": "system", "content": "你是一个智能助理，你的回答总是容易理解的、正确的、有用的和内容非常精简。"},
]

def chat_with_assistant(user_input):
    # 将用户输入添加到历史中
    history.append({"role": "user", "content": user_input})
    
    # 获取智能助理的回答
    get_assistant_reply()
    

def get_assistant_reply():
    completion = openai_client.chat.completions.create(
        model="local-model",
        messages=history,
        temperature=0.7,
        stream=True,
    )
    
    reply = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            # 流式输出回答
            print(chunk.choices[0].delta.content, end="", flush=True)
            reply += chunk.choices[0].delta.content
            
            
    # history.append({"role": "assistant", "content": reply})
    # return reply

# 开始聊天
user_input = "你好"
chat_with_assistant(user_input)
