# rag_service.py

def rag_search(prompt):
    # 获取prompt最后一个user元素
    last_ask = prompt.split("\n")[-1]
    # 获取字符串部分
    last_ask = last_ask.split(":")[1].strip()

    result = ""

    # 搜索本地文件

    # 搜索互联网

    # 搜索本地数据库

    result = f' " {result}" '

    return result
