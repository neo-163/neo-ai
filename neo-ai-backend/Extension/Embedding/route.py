from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

# 定义请求体模型
class TextRequest(BaseModel):
    text: str

# 定义响应体模型
class EmbeddingResponse(BaseModel):
    object: str = "list"
    data: list

# 初始化 FastAPI 应用和配置路由
router = APIRouter(prefix="/embed")

# 加载模型
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
# model_name = 'neo-ai/models/embedding/all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

@router.post("/v1", response_model=EmbeddingResponse)
def embed_texts(request: TextRequest):
    try:
        text = request.text
        # 生成嵌入
        embeddings = model.encode(text)
        # 格式化为openai的标准格式
        formatted_embeddings = [{"object": "embedding", "embedding": embeddings.tolist()}]
        return {"object": "list", "data": formatted_embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))