from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from usecase4 import router as usecase4_router


app = FastAPI()


# ============================================
# CORS
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# REGISTER ROUTES
# ============================================

app.include_router(usecase4_router)


# ============================================
# ROOT
# ============================================

@app.get("/")
async def root():

    return {
        "message": "RAG Backend Running"
    }
