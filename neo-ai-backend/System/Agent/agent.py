from transformers import BertTokenizer, BertForSequenceClassification
import torch

# 加载预训练的BERT模型和tokenizer
model_name = "bert-base-chinese"  # 使用中文预训练模型
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

# 定义意图标签
intent_labels = {0: "其他", 1: "语音设置"}

# 分析用户意图
def analyze_intent(query):
    # 将用户提问转换为BERT输入格式
    inputs = tokenizer(query, padding=True, truncation=True, return_tensors="pt")
    
    # 使用BERT模型进行意图分类
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
    
    # 返回意图标签
    return intent_labels[predicted_class]



def llm_agent(prompt, ai_name, ai_role, agent):
    # 测试示例
    queries = [
        "请把语速调快一点",
        "我想换一个女生的声音",
        "帮我把音量调大",
        "明天的天气怎么样？",
        "请问现在几点了？"
    ]


    for query in queries:
        intent = analyze_intent(query)
        print(f"用户提问: {query}")
        print(f"意图: {intent}")
        print(prompt)

    return intent


# 但是我觉得不准确