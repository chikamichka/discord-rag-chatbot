from pathlib import Path
from typing import Optional
import pypdf
from docx import Document


class DocumentConverter:
    """Convert various document formats to text"""
    
    @staticmethod
    def convert_pdf(file_path: Path) -> str:
        """
        Convert PDF to text
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        text = []
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text.strip():
                        text.append(f"--- Page {page_num + 1} ---\n{page_text}")
            
            return "\n\n".join(text)
        
        except Exception as e:
            raise ValueError(f"Failed to convert PDF: {str(e)}")
    
    @staticmethod
    def convert_docx(file_path: Path) -> str:
        """
        Convert DOCX to text
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Extracted text
        """
        try:
            doc = Document(file_path)
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            return "\n\n".join(paragraphs)
        
        except Exception as e:
            raise ValueError(f"Failed to convert DOCX: {str(e)}")
    
    @staticmethod
    def convert_txt(file_path: Path) -> str:
        """
        Read text file
        
        Args:
            file_path: Path to text file
            
        Returns:
            File contents
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Failed to read text file: {str(e)}")
    
    @classmethod
    def convert(cls, file_path: Path) -> str:
        """
        Convert any supported file to text
        
        Args:
            file_path: Path to file
            
        Returns:
            Extracted text
            
        Raises:
            ValueError: If file type not supported or conversion fails
        """
        suffix = file_path.suffix.lower()
        
        converters = {
            '.pdf': cls.convert_pdf,
            '.docx': cls.convert_docx,
            '.txt': cls.convert_txt,
            '.md': cls.convert_txt,
        }
        
        converter = converters.get(suffix)
        if not converter:
            raise ValueError(f"Unsupported file type: {suffix}")
        
        return converter(file_path)