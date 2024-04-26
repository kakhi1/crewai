from crewai_tools import BaseTool
import pdfplumber
from typing import List
from pydantic import BaseModel, Field

class PDFReaderTool(BaseTool, BaseModel):
    # Declare fields with default values and ensure they are recognized during initialization
    name: str = "PDF Reader Tool"
    description: str = "Reads and preprocesses PDF text from specified file paths."
    pdf_paths: List[str] = Field(...)

    # Update the initialization method to use Pydantic's data handling
    def __init__(self, **data):
        super().__init__(**data)  # Properly initialize fields with Pydantic's system

    def _run(self) -> str:
        compiled_text = ""
        for file_path in self.pdf_paths:
            with pdfplumber.open(file_path) as pdf:
                pages = [page.extract_text() for page in pdf.pages]
                processed_text = "".join(pages if pages else [''])
                compiled_text += "\n\n" + processed_text
        return compiled_text
