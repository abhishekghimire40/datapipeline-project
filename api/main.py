from typing import Annotated
from fastapi import FastAPI, UploadFile, File
import os

import helper
import config

app = FastAPI()

if not os.path.exists(config.UPLOAD_DIRECTORY):
    os.mkdir(config.UPLOAD_DIRECTORY)


@app.get("/")
async def root():
    return {"message": "Hello world"}


# method to recieve the uploaded data file
@app.post("/uploads/")
async def get_file(file: Annotated[UploadFile, File()]):
    if not file.filename:
        return {"error": "file was not uploaded"}
    # check if the file is of right type
    if not helper.check_file_type(file.content_type):
        return {"error": "unsupported media type"}

    file_path, filename = helper.get_file_name(file.filename)

    try:
        await helper.write_file(file, file_path)
    except Exception as e:
        os.remove(file_path)
        return {"error": e.__str__()}

    return {
        "filename": filename,
        "file_path": file_path,
        "content_type": file.content_type,
    }
