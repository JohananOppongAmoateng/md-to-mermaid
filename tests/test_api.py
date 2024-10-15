import pytest
import tempfile
import mermaid
from fastapi.testclient import TestClient
from unittest.mock import patch, mock_open
from api import app
from md_to_mermaid import (
    convert_to_mermaid_code,
    MermaidNode
)

client = TestClient(app)

# Example Markdown input for testing
markdown_input = {
    "title": "Test Diagram",
    "format": "Flowchart LR",
    "output_type": "html",
    "data": "# Heading 1\n## Heading 2\n"
}

def test_convert_to_mermaid_code():
    node = MermaidNode(header_level=1, header_text="Root Node")
    result = convert_to_mermaid_code(node)
    assert 'graph Flowchart LR\nNode0["Root Node"]' in result



# @patch("mermaid.Diagram.render", return_value=b"fake_image_data")
# def test_generate_image(mock_run):
#     mock_run.return_value = None  # Mock the output of subprocess.run
#     response = client.post("/generate-mermaid-diagram", json={
#             "title": "Test Image",
#             "format": "Flowchart LR",
#             "output_type": "image",
#             "data": "# Heading 1\n## Heading 2"
#         })
        
#     assert response.status_code == 200
#     assert response.content == b"fake_image_data"


def test_generate_html():
    response = client.post("/generate-mermaid-diagram", json=markdown_input)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["title"] == "Test Diagram"
    assert json_response["format"] == "Flowchart LR"
    assert "<div class=\"mermaid\">" in json_response["data"]

# Test Markdown output
def test_generate_markdown():
    markdown_input["output_type"] = "markdown"
    response = client.post("/generate-mermaid-diagram", json=markdown_input)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["format"] == "Flowchart LR"
    assert "```mermaid" in json_response["data"]
