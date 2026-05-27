from fastapi import APIRouter
from fastapi import HTTPException

from pydantic import BaseModel

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from langchain_community.vectorstores import Chroma


load_dotenv()


# ============================================
# ROUTER
# ============================================

router = APIRouter()


# ============================================
# REQUEST MODEL
# ============================================

class ChatRequest(BaseModel):

    question: str


# ============================================
# LOAD PDF
# ============================================

loader = PyPDFLoader("document.pdf")

documents = loader.load()


# ============================================
# SPLIT DOCUMENTS
# ============================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = splitter.split_documents(documents)


# ============================================
# EMBEDDINGS
# ============================================

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


# ============================================
# VECTOR STORE
# ============================================

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./chroma_db"
)


# ============================================
# RETRIEVER
# ============================================

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


# ============================================
# LLM
# ============================================

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


# ============================================
# API
# ============================================

@router.post("/chat")
async def chat(request: ChatRequest):

    try:

        question = request.question


        # RETRIEVE DOCS
        retrieved_docs = retriever.invoke(question)

        context = "\n\n".join([
            doc.page_content
            for doc in retrieved_docs
        ])


        # PROMPT
        prompt = f"""
        Answer ONLY from the provided context.

        If answer is not present,
        say "I don't know."

        Context:
        {context}

        Question:
        {question}
        """


        # LLM RESPONSE
        response = llm.invoke(prompt)

        answer = response.content


        return {
            "answer": answer,
            "sources": [
                doc.page_content[:300]
                for doc in retrieved_docs
            ]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
