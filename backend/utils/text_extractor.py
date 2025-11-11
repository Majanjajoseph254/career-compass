import PyPDF2
import docx
import os

def extract_text(file_path):
    """Extract text from PDF, DOCX, or TXT files"""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_extension == '.pdf':
            return extract_from_pdf(file_path)
        elif file_extension == '.docx':
            return extract_from_docx(file_path)
        elif file_extension == '.txt':
            return extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    except Exception as e:
        raise Exception(f"Error extracting text: {str(e)}")

def extract_from_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_from_docx(file_path):
    """Extract text from DOCX file"""
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_from_txt(file_path):
    """Extract text from TXT file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()