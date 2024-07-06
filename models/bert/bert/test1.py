import sys
import torch
from transformers import BertTokenizer, BertForSequenceClassification

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


def change_volume():
    print("正在调整音量...")


def enable_voice_recognition():
    print("正在启用语音识别...")


def disable_voice_recognition():
    print("正在关闭语音识别...")


def play_music():
    print("正在播放音乐...")


def search_information():
    print("正在搜索信息...")


def check_weather():
    print("正在查询天气...")


def set_alarm():
    print("正在设置闹钟...")


def open_app():
    print("正在打开应用...")


def send_message():
    print("正在发送短信...")


def make_call():
    print("正在拨打电话...")


def translate_language():
    print("正在翻译语言...")


def record_video():
    print("正在录制视频...")


def play_video():
    print("正在播放视频...")


# 意图到函数的映射
intent_to_function = {
    "创建用户": create_user,
    "执行sql": execute_sql,
    "查询知识库": query_knowledge_base,
    "切换语音": switch_voice,
    "变换发音人": change_speaker,
    "调节音量": change_volume,
    "启用语音识别": enable_voice_recognition,
    "关闭语音识别": disable_voice_recognition,
    "播放音乐": play_music,
    "搜索信息": search_information,
    "查询天气": check_weather,
    "设置闹钟": set_alarm,
    "打开应用": open_app,
    "发送短信": send_message,
    "拨打电话": make_call,
    "翻译语言": translate_language,
    "录制视频": record_video,
    "播放视频": play_video
}

# 初始化tokenizer和模型
model_path = "./model/finetuned_model1"
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)

# 获取标签列表
labels = list(intent_to_function.keys())

# 意图识别函数


def predict_intent(question):
    inputs = tokenizer(question, return_tensors="pt",
                       truncation=True, padding=True, max_length=128)
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
print("测试第一次微调的模型:")
handle_question("我需要运行一条SQL语句")
handle_question("如何创建一个新用户")
handle_question("请把音量调大一点")
