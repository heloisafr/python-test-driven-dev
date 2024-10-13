import os
import pytest


def test_call_required_send_required_ok(client, test_folder) -> None:
    """
    In this end-point it is required to send a file
    Tests if send file is ok
    """
    file = "sample_file.txt"
    file_path = os.path.join(test_folder, file)
    with open(file_path, "rb") as f:
        response = client.post("/api/file/required", files={"sample_file": (file, f)})

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["filename"] == "sample_file.txt"
    assert response.json()["content_type"] == "text/plain"


def test_call_required_missing_error(client, test_folder) -> None:
    """
    In this end-point it is required to send a file
    Tests the error when the file is missing
    """
    response = client.post("/api/file/required")

    assert response.status_code == 422
    assert response.json()["detail"][0]['type'] == "missing"
    assert response.json()["detail"][0]['msg'] == "Field required"
    assert response.json()["detail"][0]['loc'][1] == "sample_file"


def test_call_required_content_type_error(client, test_folder) -> None:
    """
    In this end-point is required to send a file
    Tests the error when the file's content_type is unexpected
    """
    file = "sample_file.txt"
    file_path = os.path.join(test_folder, file)
    with open(file_path, "rb") as f:
        response = client.post(
            "/api/file/required",
            files={"sample_file": (file, f, "application/json")}
        )

    assert response.status_code == 422
    assert response.json()["detail"] == "Sample file should be plain text."


def test_call_optional_send_empty_ok(client, test_folder) -> None:
    """
    O envio do arquivo é opcional, requisição sem o arquivo
    """
    response = client.post("/api/file/optional")

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["filename"] is None
    assert response.json()["content_type"] is None


def test_call_optional_send_file_ok(client, test_folder) -> None:
    """
    O envio do arquivo é opcional, requisição com arquivo
    """
    file = "sample_file.txt"
    file_path = os.path.join(test_folder, file)
    with open(file_path, "rb") as f:
        response = client.post("/api/file/optional", files={"sample_file": (file, f)})

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["filename"] == "sample_file.txt"
    assert response.json()["content_type"] == "text/plain"


def test_call_multiple_file_parameter_send_only_required_ok(client, test_folder) -> None:
    """
    Nesse end-point temos 2 parametros, um por arquivo
    Um arquivo é obrigatório enquanto outro é opcional
    """
    file = "sample_file.txt"
    file_path = os.path.join(test_folder, file)
    with open(file_path, "rb") as f:
        response = client.post("/api/file/multiple-file-parameter", files={"sample_file_one": (file, f)})

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["filename_one"] == "sample_file.txt"
    assert response.json()["content_type_one"] == "text/plain"
    assert response.json()["filename_two"] is None
    assert response.json()["content_type_two"] is None


def test_call_multiple_file_parameter_send_both_ok(client, test_folder) -> None:
    """
    Nesse end-point temos 2 parametros, um por arquivo
    Um arquivo é obrigatório enquanto outro é opcional
    """
    file_one = "sample_file.txt"
    file_path_one = os.path.join(test_folder, file_one)
    file_two = "sample_file_two.txt"
    file_path_two = os.path.join(test_folder, file_two)
    with open(file_path_one, "rb") as f1, open(file_path_two, "rb") as f2:
        response = client.post(
            "/api/file/multiple-file-parameter",
            files={
               "sample_file_one": ("sample_file_one.txt", f1),
               "sample_file_two": ("sample_file_two.txt", f2)
            }
        )

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["filename_one"] == "sample_file_one.txt"
    assert response.json()["content_type_one"] == "text/plain"
    assert response.json()["filename_two"] == "sample_file_two.txt"
    assert response.json()["content_type_two"] == "text/plain"


def test_call_multiple_optional_send_empty_ok(client, test_folder) -> None:
    """
    Nesse end-point temos 1 parametro que recebe mais de um arquivo
    O envio de arquivos é opcional
    """

    response = client.post(
        "/api/file/multiple/optional",
        files={}
    )
    print(response.text)

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["filenames"] == []


def test_call_multiple_optional_send_one_ok(client, test_folder) -> None:
    """
    Nesse end-point temos 1 parametro que recebe mais de um arquivo
    O envio de arquivos é opcional
    """
    file_one = "sample_file.txt"
    file_path_one = os.path.join(test_folder, file_one)
    with open(file_path_one, "rb") as f1:
        response = client.post(
            "/api/file/multiple/optional",
            files={
               "sample_files": ("sample_file_one.txt", f1)}
           )

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["filenames"] == ["sample_file_one.txt"]


def test_call_multiple_optional_send_two_ok(client, test_folder) -> None:
    """
    Nesse end-point temos 1 parametro que recebe mais de um arquivo
    O envio de arquivos é opcional
    """
    file_one = "sample_file.txt"
    file_path_one = os.path.join(test_folder, file_one)
    file_two = "sample_file_two.txt"
    file_path_two = os.path.join(test_folder, file_two)
    with open(file_path_one, "rb") as f1, open(file_path_two, "rb") as f2:
        response = client.post(
            "/api/file/multiple/optional",
            files=[
                ("sample_files", ("sample_file_one.txt", f1)),
                ("sample_files", ("sample_file_two.txt", f2))
            ]
        )

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["filenames"] == ["sample_file_one.txt", "sample_file_two.txt"]


def test_call_multiple_required_send_one_ok(client, test_folder) -> None:
    """
    Nesse end-point temos 1 parametro que recebe mais de um arquivo
    O envio de ao menos um arquivos é obrigatorio
    """
    file_one = "sample_file.txt"
    file_path_one = os.path.join(test_folder, file_one)
    with open(file_path_one, "rb") as f1:
        response = client.post(
            "/api/file/multiple/required",
            files={
               "sample_files": ("sample_file_one.txt", f1)}
           )

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["filenames"] == ["sample_file_one.txt"]


def test_mix_optional_send_all_ok(client, test_folder) -> None:
    """
    Nesse end-point temos 3 parametros
      :param: name recebe um texto
      :param: sample_file recebe um arquivo
      :param: multiple_files recebe um ou mais arquivos
    O envio de dados é opcional
    """
    file_one = "sample_file.txt"
    file_path_one = os.path.join(test_folder, file_one)
    file_two = "sample_file_two.txt"
    file_path_two = os.path.join(test_folder, file_two)
    with open(file_path_one, "rb") as f1, open(file_path_two, "rb") as f2:
        response = client.post(
            "/api/file/mix/optional",
            data={"name": "Juliana"},
            files=[
                ("sample_file", ("sample_file_alone.txt", f1)),
                ("multiple_files", ("sample_file_one.txt", f1)),
                ("multiple_files", ("sample_file_two.txt", f2))
            ]
        )

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["name"] == "Juliana"
    assert response.json()["sample_file"] == "sample_file_alone.txt"
    assert response.json()["multiple_files"] == ["sample_file_one.txt", "sample_file_two.txt"]


def test_mix_send_nothing(client, test_folder) -> None:
    """
    Nesse end-point temos 3 parametros
      :param: name recebe um texto
      :param: sample_file recebe um arquivo
      :param: multiple_files recebe um ou mais arquivos
    O envio de dados é opcional
    """
    response = client.post(
        "/api/file/mix/optional"
    )

    print(response.json())
    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["name"] is None
    assert response.json()["sample_file"] is None
    assert response.json()["multiple_files"] == []


def test_mix_required(client, test_folder) -> None:
    """
    Nesse end-point temos 3 parametros
      :param: name recebe um texto
      :param: sample_file recebe um arquivo
      :param: multiple_files recebe um ou mais arquivos
    O envio de dados é obrigatorio
    """
    file_one = "sample_file.txt"
    file_path_one = os.path.join(test_folder, file_one)
    file_two = "sample_file_two.txt"
    file_path_two = os.path.join(test_folder, file_two)
    with open(file_path_one, "rb") as f1, open(file_path_two, "rb") as f2:
        response = client.post(
            "/api/file/mix/required",
            data={"name": "Juliana"},
            files=[
                ("sample_file", ("sample_file_alone.txt", f1)),
                ("multiple_files", ("sample_file_one.txt", f1)),
                ("multiple_files", ("sample_file_two.txt", f2))
            ]
        )

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["name"] == "Juliana"
    assert response.json()["sample_file"] == "sample_file_alone.txt"
    assert response.json()["multiple_files"] == ["sample_file_one.txt", "sample_file_two.txt"]

