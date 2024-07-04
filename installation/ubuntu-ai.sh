#!/bin/bash
# 服务器：Ubuntu Server 22.04 LTS 64bit

# ## Nginx ##

# 更新软件包
sudo apt update

# 安装依赖项（如果尚未安装）：
sudo apt install -y curl gnupg2 ca-certificates lsb-release

# 安装Nginx
sudo apt install -y nginx

# 检查Nginx版本
nginx -v

# 配置防火墙：如果使用 UFW 作为防火墙，且开启的情况下
# sudo ufw allow 'Nginx Full'

# 验证Nginx状态
sudo systemctl status nginx

# 启动Nginx
sudo systemctl start nginx

# 设置Nginx开机自启
sudo systemctl enable nginx

# ## AI System Backend ##

git clone https://github.com/neo-163/neo-ai.git

cd neo-ai/

cd neo-ai-backend/

pip install -r requirements.txt

cp /home/ubuntu/neo-ai/neo-ai-backend/Extension/LLM/setting_sample.py /home/ubuntu/neo-ai/neo-ai-backend/Extension/LLM/setting.py 
cp /home/ubuntu/neo-ai/neo-ai-backend/Extension/RAG/setting_sample.py /home/ubuntu/neo-ai/neo-ai-backend/Extension/RAG/setting.py 
cp /home/ubuntu/neo-ai/neo-ai-backend/Extension/Speech/setting_sample.py /home/ubuntu/neo-ai/neo-ai-backend/Extension/Speech/setting.py 

# 设置好相关的key，启动FastAPI
# nohup python3 main.py &

# test backend isntallation
# http://ip:1888/demo/

# ## AI System Frontend ##
sudo mkdir /usr/share/nginx/web

#上传dist文件到：/home/ubuntu/
# mv /home/ubuntu/dist /usr/share/nginx/web/
