import aiofiles
import uuid
import os
import config

# check if the file is supported or not


def check_file_type(content_type: str | None):
    if not content_type:
        return False
    content_type = content_type.lower()
    file_types = ["csv", "spreadsheet", "excel"]
    if not any(file_type in content_type for file_type in file_types):
        return False
    return True


def get_file_name(name: str | None):
    random_id = str(uuid.uuid4())
    if name:
        filename = random_id + "_" + os.path.basename(name)
    else:
        filename = random_id + "_"
    return (os.path.join(config.UPLOAD_DIRECTORY, filename), filename)


# function to read and write to a file
async def write_file(file, file_path):
    async with aiofiles.open(file_path, "wb") as f:
        while True:
            chunk = await file.read(config.CHUNK_SIZE)
            if not chunk:  # if we reach the end of file then break
                break
            await f.write(chunk)
