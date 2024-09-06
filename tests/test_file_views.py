import os
import pytest


def test_send_file_required_ok(client, test_folder) -> None:
    file = "sample_file.txt"
    file_path = os.path.join(test_folder, file)
    with open(file_path, "rb") as f:
        response = client.post("/api/file/required", files={"sample_file": (file, f)})

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["filename"] == "sample_file.txt"
    assert response.json()["content_type"] == "text/plain"


# def test_send_file_optional_ok(client, test_folder) -> None:
#     # file = "sample_file.txt"
#     # file_path = os.path.join(test_folder, file)
#     # with open(file_path, "rb") as f:
#     # response = client.post("/api/file/required", files={"sample_file": (file, f)})
#     response = client.post("/api/file/required", files={})
#
#     assert response.status_code == 200
#     assert response.json()["ok"] is True
#     assert response.json()["filename"] == "sample_file.txt"
#     assert response.json()["content_type"] == "text/plain"
