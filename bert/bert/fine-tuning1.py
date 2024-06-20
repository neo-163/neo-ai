from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
import torch
import json

# 读取数据集
with open('../training_data/data1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 将数据分为训练集和测试集
questions, labels = zip(*data)
questions_train, questions_test, labels_train, labels_test = train_test_split(questions, labels, test_size=0.1)

# 加载tokenizer和模型：bert-base-uncased，bert-large-uncased
base_model = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(base_model)
model = BertForSequenceClassification.from_pretrained(base_model, num_labels=len(set(labels)))

# 准备训练和测试数据
train_encodings = tokenizer(list(questions_train), truncation=True, padding=True, max_length=128)
test_encodings = tokenizer(list(questions_test), truncation=True, padding=True, max_length=128)

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
test_dataset = Dataset(test_encodings, labels_test)

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
    eval_dataset=test_dataset
)

# 训练模型
trainer.train()

# 保存模型
model_path = "./model/finetuned_model1"
model.save_pretrained(model_path)
tokenizer.save_pretrained(model_path)
