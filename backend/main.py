from fastapi import FastAPI
from routes import user, item, auth

app = FastAPI()

# Include routes
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(item.router, prefix="/items", tags=["Items"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI App"}
