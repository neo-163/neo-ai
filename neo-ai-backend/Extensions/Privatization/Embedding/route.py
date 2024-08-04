from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from text2vec import SentenceModel

# 定义请求体模型
class TextRequest(BaseModel):
    input: list[str]

# 定义响应体模型
class EmbeddingResponse(BaseModel):
    object: str = "list"
    model: str
    data: list

# 初始化 FastAPI 应用和配置路由
router = APIRouter(prefix="/embed")

Embedding_Model = "text2vec-base-chinese"
# 下载模型：https://modelscope.cn/models/Jerry0/text2vec-base-chinese/files
# 加载模型
model_name = "Models/embedding/" + Embedding_Model
model = SentenceModel(model_name)

@router.post("/v1/", response_model=EmbeddingResponse)
async def embed_texts(request: TextRequest):
    try:
        texts = request.input
        # 生成嵌入
        embeddings = model.encode(texts)
        # 格式化为openai的标准格式
        formatted_embeddings = [
            {"object": "embedding", "index": idx, "embedding": embedding.tolist()}
            for idx, embedding in enumerate(embeddings)
        ]
        return {
            "object": "list",
            "model": Embedding_Model,
            "data": formatted_embeddings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
