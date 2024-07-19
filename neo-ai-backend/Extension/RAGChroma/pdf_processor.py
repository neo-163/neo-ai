import PyPDF2
import requests
import json
import time
import chromadb
import numpy as np
import re
from Extension.RAGChroma.setting import Erniebot_API_KEY, Erniebot_SECRET_KEY

# 初始化 ChromaDB
client = chromadb.Client()
# client = chromadb.PersistentClient(path="mydb1.db")

# 获取或创建 collection
collection = client.get_or_create_collection(name="pdf_documents")

# 读取PDF文件并提取文本
def extract_text_from_pdf(pdf_path):
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

# 将PDF文本分块并存储到向量数据库
def store_pdf_chunks_in_db(pdf_text, chunk_size=1000):
    # 使用正则表达式根据多个分隔符分割文本，匹配一个或多个连续的换行符。
    separator_pattern = r'\n+'
    paragraphs = re.split(separator_pattern, pdf_text)
    
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()  # 去除段落前后的空格
        if len(current_chunk) + len(paragraph) <= chunk_size:
            current_chunk += paragraph + "\n"
        else:
            chunks.append(current_chunk)
            current_chunk = paragraph + "\n"

    if current_chunk:
        chunks.append(current_chunk)

    for chunk in chunks:
        # 使用正则表达式根据多个分隔符分割文本
        sub_chunks = re.split(separator_pattern, chunk)
        
        for sub_chunk in sub_chunks:
            sub_chunk = sub_chunk.strip()  # 去除子块前后的空格
            if sub_chunk:  # 确保子块不为空
                vector = get_erniebot_embedding(sub_chunk)
                if vector is not None:
                    collection.add(
                        documents=[sub_chunk],
                        ids=[str(hash(sub_chunk))],
                        embeddings=[vector.tolist()]
                    )

# 获取文心一言的访问令牌
def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": Erniebot_API_KEY, "client_secret": Erniebot_SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

# 获取文心一言的嵌入向量
def get_erniebot_embedding(text, chunk_size=512, retries=1):
    access_token = get_access_token()
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/embedding-v1?access_token={access_token}"
    headers = {'Content-Type': 'application/json'}
    
    # 将文本分割成多个块
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    vectors = []
    for chunk in chunks:
        data = {"input": [chunk]}
        for attempt in range(retries):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data))
                if response.status_code == 200:
                    response_data = response.json()
                    if "data" in response_data:
                        vectors.append(response_data["data"][0]["embedding"])
                    elif "result" in response_data and "data" in response_data["result"]:
                        vectors.append(response_data["result"]["data"][0]["embedding"])
                    break
                else:
                    print(f"Failed to get embedding: {response.status_code} - {response.text}")
                    time.sleep(1)  # 等待一段时间后重试
            except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                print(f"Error: {e}")
                time.sleep(1)  # 等待一段时间后重试
    
    if vectors:
        return np.mean(vectors, axis=0)  # 返回所有块向量的平均值
    else:
        return None

# 生成PDF摘要和用户可能关心的问题
def generate_summary_and_questions(pdf_text):
    prompt = f"请根据PDF文本，总结简要的摘要，并提出您（用户）可能关心的3个问题：\n{pdf_text}"
    response = get_erniebot_response(prompt)
    return response


# 获取文心一言的流式响应
def get_stream_response(prompt, ai_name, ai_role, retries=3):
    model = "ernie-speed-128k"
    access_token = get_access_token()
    if not access_token:
        return None
    source = "&sourceVer=0.0.1&source=app_center&appName=streamDemo"
    base_url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{model}"
    url = f"{base_url}?access_token={access_token}{source}"
    data = {
        "system": f"{ai_name} {ai_role}",
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }
    payload = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, data=payload, stream=True)
            if response.status_code == 200:
                return response
            else:
                print(f"Failed to get stream response: {response.status_code} - {response.text}")
                time.sleep(1)  # 等待一段时间后重试
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            time.sleep(1)  # 等待一段时间后重试
    return None

# 获取文心一言的响应
def get_erniebot_response(prompt):
    response = get_stream_response(prompt, "ErnieBot", "assistant")
    for chunk in response.iter_lines():
        chunk = chunk.decode("utf8")
        if chunk[:5] == "data:":
            chunk = chunk[5:]
        yield chunk
        time.sleep(0.01)


# 使用 ChromaDB 进行查询
def query_chromadb(question):
    # 在 ChromaDB 中查找与问题嵌入向量最相似的段落
    results = collection.query(
        query_texts=[question],
        n_results=5
    )
    return results

def delete_all_documents():
    """删除全部数据"""
    while True:
        documents = collection.get()
        if not documents['ids']:
            break
        collection.delete(ids=documents['ids'])
