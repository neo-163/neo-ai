# test.py
import sys
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification

sys.stdout.reconfigure(encoding='utf-8')

# 模拟功能函数
def create_user():
    print("正在创建用户...")

def execute_sql():
    print("正在执行SQL...")

def query_knowledge_base():
    print("正在查询知识库...")

def switch_voice():
    print("正在切换语音...")

def change_speaker():
    print("正在变换发音人...")

def change_speed():
    print("正在调整语速...")

def change_volume():
    print("正在调整音量...")

def change_pitch():
    print("正在调整语调...")

# 意图到函数的映射
intent_to_function = {
    "创建用户": create_user,
    "执行sql": execute_sql,
    "查询知识库": query_knowledge_base,
    "切换语音": switch_voice,
    "变换发音人": change_speaker,
    "变换语速": change_speed,
    "变换音量": change_volume,
    "变换语调": change_pitch
}

# 初始化tokenizer和模型
model_path = "./saved_model"
tokenizer = RobertaTokenizer.from_pretrained(model_path)
model = RobertaForSequenceClassification.from_pretrained(model_path)

# 定义标签
labels = ["创建用户", "执行sql", "查询知识库", "切换语音", "变换发音人", "变换语速", "变换音量", "变换语调"]

# 意图识别函数
def predict_intent(question):
    inputs = tokenizer(question, return_tensors="pt", truncation=True, padding=True, max_length=128)
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)
    predicted_index = predictions.item()
    if predicted_index < len(labels):
        predicted_intent_label = labels[predicted_index]
    else:
        predicted_intent_label = "未知意图"
    return predicted_intent_label

# 意图识别并调用相应功能
def handle_question(question):
    print(f"问题: {question}")
    predicted_intent = predict_intent(question)
    print(f"预测的意图: {predicted_intent}")

    if predicted_intent in intent_to_function:
        intent_to_function[predicted_intent]()
    else:
        print("未识别的意图，无法执行相关操作。")

# 示例使用
# handle_question("我需要运行一条SQL语句")
# handle_question("请帮我创建一个新用户")
# handle_question("切换到中文语音")

handle_question("我需要运行一条SQL语句")
handle_question("如何创建一个新用户")
handle_question("改变语音的发音人")
