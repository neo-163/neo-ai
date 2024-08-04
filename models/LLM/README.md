启动Qwen2大模型
n_ctx=20480代表单次回话最大20480个Token数量

## 本地部署 通义千问2

https://modelscope.cn/models/qwen/qwen2-7b-instruct-gguf/files

```
python -m llama_cpp.server --host 0.0.0.0 --model ./qwen2-7b-instruct-q5_k_m.gguf --n_ctx 20480 --port 8100
```
https://modelscope.cn/models/qwen/qwen2-72b-instruct-gguf/files


## 本地部署 llama3

https://modelscope.cn/models/LLM-Research/Meta-Llama-3.1-8B-Instruct/files
```
python -m llama_cpp.server --host 0.0.0.0 --model ./llama3-zh.Q4_K_M.gguf --n_ctx 20480 --port 8100
```
