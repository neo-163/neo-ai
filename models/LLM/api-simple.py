from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from openai import OpenAI
import asyncio

app = FastAPI()

# 设置 OpenAI 客户端
openai_client = OpenAI(base_url="http://127.0.0.1:8100/v1", api_key="not-needed")

# 对话历史：设定系统角色是一个智能助理
history = [
    {"role": "system", "content": "你是一个智能助理,你的回答总是容易理解的、正确的、有用的和内容非常精简。"},
]

async def generate_reply(user_input):
    # 将用户输入添加到历史中
    history.append({"role": "user", "content": user_input})

    # 获取智能助理的回答
    completion = openai_client.chat.completions.create(
        model="local-model",
        messages=history,
        temperature=0.7,
        stream=True,
    )

    reply = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            chunk_content = chunk.choices[0].delta.content

            # 实时打印到控制台
            # print(chunk_content, end="", flush=True)
            # 实时发送到客户端
            yield f"data: {chunk_content}\n\n"
            # 暂停一下，确保内容被立即发送。这个暂停不会阻塞事件循环，而是允许其他任务执行。
            await asyncio.sleep(0) 
            
            reply += chunk_content

    # print(reply)
    history.append({"role": "assistant", "content": reply})

@app.post("/llm_private/chat1")
async def chat(request: Request):
    user_input = (await request.json())["message"]
    return StreamingResponse(generate_reply(user_input), media_type="text/event-stream", headers={"X-Accel-Buffering": "no"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
    