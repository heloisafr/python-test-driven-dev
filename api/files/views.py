from fastapi import APIRouter, UploadFile

router_files = APIRouter()


@router_files.post("/required")
def add_file_required(sample_file: UploadFile):
    return ({
        "ok": True,
        "filename": sample_file.filename,
        "content_type": sample_file.content_type
    })


# @router_files.post("/opt")
# def add_file_optional(sample_file: UploadFile = None):
#     return {
#         "ok": True,
#         # "filename": sample_file.filename,
#         # "content_type": sample_file.content_type
#     }
