from fastapi import APIRouter, Form, File, HTTPException, status, UploadFile

router_files = APIRouter()


@router_files.post("/required")
def add_file_required(sample_file: UploadFile = File(...)):
    """
    A assinatura do methodo pode ser:
    sample_file: UploadFile = File(...) (explicitamente dizendo que é um arquivo e obrigatorio)
    sample_file: UploadFile (sem nada mesmo, a fastapi entende que é obrigatório)
    """
    # This is a naive way to test the content_type
    if sample_file.content_type != "text/plain":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Sample file should be plain text."
        )

    return ({
        "ok": True,
        "filename": sample_file.filename,
        "content_type": sample_file.content_type
    })


@router_files.post("/optional")
def add_file_optional(sample_file: UploadFile = None):
    """
    O envio do arquivo é opcional
    """
    filename = None
    content_type = None
    if sample_file is not None:
        filename = sample_file.filename
        content_type = sample_file.content_type

    return {
        "ok": True,
        "filename": filename,
        "content_type": content_type
    }


@router_files.post("/multiple-file-parameter")
def add_two_files(
        sample_file_one: UploadFile,
        sample_file_two: UploadFile = None
):
    """
    Nesse end-point temos 2 parametros, um por arquivo
    Um arquivo é obrigatório enquanto outro é opcional
    """
    filename_two = None
    content_type_two = None
    if sample_file_two is not None:
        filename_two = sample_file_two.filename
        content_type_two = sample_file_two.content_type

    return {
        "ok": True,
        "filename_one": sample_file_one.filename,
        "content_type_one": sample_file_one.content_type,
        "filename_two": filename_two,
        "content_type_two": content_type_two
    }


@router_files.post("/multiple/optional")
def add_file_multiple_optional(
        sample_files: list[UploadFile] = None
):
    """
    Nesse end-point temos 1 parametro que recebe mais de um arquivo
    O envio de arquivos é opcional
    """
    filenames = []
    if sample_files is not None:
        for sample_file in sample_files:
            filenames.append(sample_file.filename)

    return {
        "ok": True,
        "filenames": filenames
    }


@router_files.post("/multiple/required")
def add_file_multiple_optional(
        sample_files: list[UploadFile]
):
    """
    Nesse end-point temos 1 parametro que recebe mais de um arquivo
    O envio de ao menos um arquivos é obrigatorio
    """
    filenames = []
    for sample_file in sample_files:
        filenames.append(sample_file.filename)

    return {
        "ok": True,
        "filenames": filenames
    }


@router_files.post("/mix/optional")
def add_mix(
    name: str = Form(default=None),
    sample_file: UploadFile = None,
    multiple_files: list[UploadFile] = None
):
    """
    Nesse end-point temos 3 parametros
     :param: name recebe um texto
     :param: sample_file recebe um arquivo
     :param: multiple_files recebe um ou mais arquivos
    O envio de dados é opcional
    """

    filenames = []
    for f in multiple_files:
        filenames.append(f.filename)

    filename = None
    if sample_file is not None:
        filename = sample_file.filename

    return {
        "ok": True,
        "name": name,
        "sample_file": filename,
        "multiple_files": filenames
    }


@router_files.post("/mix/required")
def add_mix(
    sample_file: UploadFile,
    multiple_files: list[UploadFile],
    name: str = Form(),
):
    """
    Nesse end-point temos 3 parametros
     :param: name recebe um texto
     :param: sample_file recebe um arquivo
     :param: multiple_files recebe um ou mais arquivos
    O envio de dados é obrigatorio
    """

    filenames = []
    for f in multiple_files:
        filenames.append(f.filename)

    filename = sample_file.filename

    return {
        "ok": True,
        "name": name,
        "sample_file": filename,
        "multiple_files": filenames
    }
