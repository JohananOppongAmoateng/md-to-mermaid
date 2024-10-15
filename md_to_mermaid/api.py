import os
import tempfile
import subprocess
import python_mermaid
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from md_to_mermaid import (
    build_MermaidNode_from_md_string,
    convert_to_mermaid_code
    )

app = FastAPI()

class MarkdownInput(BaseModel):
    title: str
    format: str
    output_type: str
    data: str


class MermaidResponse(BaseModel):
    title: str
    format: str
    data: Union[str | bytes]
    md_data: str


@app.post("/generate-mermaid-diagram")
async def generate_mermaid_diagram(markdown: MarkdownInput):
    mermaid_tree = build_MermaidNode_from_md_string(markdown.data)

    mermaid_code = convert_to_mermaid_code(mermaid_tree)

    response = MermaidResponse(
        title=markdown.title,
        format=markdown.format,
        md_data=markdown.data,
        data=""  # This will be updated based on the output type
    )

    # if markdown.output_type == "image":
    #     image_response = generate_image(mermaid_code)
    #     response.data = image_response["data"]
        
    if markdown.output_type == "html":
        html_response = generate_html(mermaid_code)
        response.data = html_response["data"]

    elif markdown.output_type == "markdown":
        markdown_response = generate_markdown(mermaid_code)
        response.data = markdown_response["data"]
    else:
        raise HTTPException(status_code=400, 
                                            detail="Invalid output_type.Use image, markdown or html.")
    return response


def generate_markdown(mermaid_code: str) -> dict:
    markdown_content = f"```mermaid\n{mermaid_code}\n```"
    return {"data": markdown_content, "format": "markdown"}


# def generate_image(mermaid_code: str) -> dict:
#     diagram = python_mermaid.Diagram(mermaid_code)
#     image_data = diagram.render(format="png")
#     return {"data": image_data, "format": "image"}


def generate_html(mermaid_code: str) -> dict:
    html_content = f"<div class=\"mermaid\">{mermaid_code}</div>"
    return {"data": html_content, "format": "html"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



