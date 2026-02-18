from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, status
from dotenv import load_dotenv
import os


from sqlalchemy.future import select
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
    return {"message": "Hello from server"}


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
        helper.file_cleanup(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="couldn't save file try again",
        )

    # creating a sqlalchemy model instance
    try:

        with db.begin():  # commit will happen automatically if everything in the block succeeds else rollback
            data_item = models.Dataset(
                original_file_name=filename, stored_path=file_path
            )
            # adding object to session
            db.add(data_item)
            db.flush()  # flush helps to get id and all without commiting
            # creating a job for the dataset that user provided
            job_item = models.ETLJob(
                dataset_id=data_item.id, status=models.Status.PENDING
            )
            # adding job obect to session
            db.add(job_item)
            db.flush()

    except Exception as e:

        # delete the file that was stored
        helper.file_cleanup(file_path=file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal server error",
        )

    return job_item


@app.get(
    "/jobs/{job_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.SingleJobResponse,
)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(models.ETLJob).where(models.ETLJob.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="job with provided id is not available",
        )
    return job
