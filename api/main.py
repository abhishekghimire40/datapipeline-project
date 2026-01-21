from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, status
import os

from sqlalchemy.orm import Session
from database import Base, engine, get_db

import schemas
import models
import helper
import config

Base.metadata.create_all(bind=engine)

app = FastAPI()

# making sure the directory to save uploaded file is created and present
if not os.path.exists(config.UPLOAD_DIRECTORY):
    os.mkdir(config.UPLOAD_DIRECTORY)


@app.get("/")
async def root():
    return {"message": "Hello world"}


# method to recieve the uploaded data file
@app.post(
    "/uploads/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UploadResponse,
)
async def get_file(file: Annotated[UploadFile, File()], db: Session = Depends(get_db)):
    # check if file is there or not
    if not file.filename:
        raise HTTPException(status_code=400, detail="no file found")
    # check if the file is of right type
    if not helper.check_file_type(file.content_type):
        raise HTTPException(status_code=415, detail="unsupported media type")

    # extract file name and the path to be save
    file_path, filename = helper.get_file_name(file.filename)

    # create a file and write data into it. if failed remove the created file
    try:
        await helper.write_file(file, file_path)
    except Exception as e:
        os.remove(file_path)
        return {"error": e.__str__()}

    # creating a sqlalchemy model instance
    data_item = models.Dataset(original_file_name=filename, stored_path=file_path)
    # adding object to session
    db.add(data_item)
    # commit changes to the database
    db.commit()

    # creating a job for the dataset that user provided
    job_item = models.ETLJob(dataset_id=data_item.id, status="PENDING")
    # adding job obect to session
    db.add(job_item)
    # commiting the changes to the database
    db.commit()

    return job_item
