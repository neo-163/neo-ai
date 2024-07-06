from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
import torch
import json

# 加载已经训练好的模型和tokenizer
model_path = "./model1/finetuned_model1"
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)

# 读取新的数据集
with open('../training_data/data2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 将数据分为训练集和验证集
questions, labels = zip(*data)
questions_train, questions_val, labels_train, labels_val = train_test_split(questions, labels, test_size=0.2)

# 准备训练和验证数据
train_encodings = tokenizer(list(questions_train), truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(list(questions_val), truncation=True, padding=True, max_length=128)

# 创建标签到索引的映射
label_to_index = {label: idx for idx, label in enumerate(set(labels))}

class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = [label_to_index[label] for label in labels]

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = Dataset(train_encodings, labels_train)
val_dataset = Dataset(val_encodings, labels_val)

# 设置训练参数
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    do_train=True,
    do_eval=True,
    evaluation_strategy="epoch"
)

# 初始化Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

# 微调模型
trainer.train()

# 保存微调后的模型
model_path = "./model/finetuned_model2"
model.save_pretrained(model_path)
tokenizer.save_pretrained(model_path)