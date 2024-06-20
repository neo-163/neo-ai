from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File
import os
from Extension.RAG.pdf_processor import extract_text_from_pdf, store_pdf_chunks_in_db, generate_summary_and_questions, query_chromadb, delete_all_documents, get_erniebot_response
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/rag")

class RequestData(BaseModel):
    question: str


@router.post("/")
async def root():
    return {"code": 200, "result": "Neo AI!"}
    
@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return {"code": 400, "error": "Invalid file type. Only PDF files are allowed."}

    # Save the uploaded file
    file_path = f"Resource/Doc/{file.filename}"
    with open(file_path, "wb") as buffer:
        contents = await file.read()
        buffer.write(contents)

    # Process the PDF file
    pdf_text = extract_text_from_pdf(file_path)
    delete_all_documents()
    store_pdf_chunks_in_db(pdf_text)
    summary_and_questions = generate_summary_and_questions(pdf_text)

    # Remove the saved file
    os.remove(file_path)

    return StreamingResponse(summary_and_questions)


@router.post("/ask")
async def query_pdf(request: RequestData):
    question = request.question
    results = query_chromadb(question)
    if results:
        # Combine query results and user question into a prompt
        query_texts = [doc for doc in results['documents'][0]]
        prompt = f"根据以下查询结果和用户问题，请给出回答：\n查询结果：\n{''.join(query_texts)}\n用户问题：{question}"

        # Call the LLM (e.g., ErnieBot) for answering
        answer = get_erniebot_response(prompt)
        return StreamingResponse(answer)
    else:
        return {"error": "No relevant results found."}
