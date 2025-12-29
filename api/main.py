from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello world"}


# method to recieve the uploaded data file
@app.post("/uploads/")
async def get_file(file: UploadFile):
    return {"filename": file.filename}
