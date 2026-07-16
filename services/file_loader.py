import os
import logging
from docx import Document

logger = logging.getLogger(__name__)

class UnsupportedFileTypeError(Exception):
    """Raised when the loaded file type is not supported."""
    pass

class FileLoadError(Exception):
    """Raised when there is a generic error loading the file."""
    pass

class FileLoaderService:
    """Service responsible for loading text from various file formats (.txt, .md, .docx)."""

    @staticmethod
    def load_file(file_path: str) -> str:
        """
        Loads and returns the text content of a file.
        Supports .txt, .md, .docx.
        
        Raises FileNotFoundError, PermissionError, UnsupportedFileTypeError, or FileLoadError.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        _, ext = os.path.splitext(file_path.lower())
        
        try:
            if ext in ('.txt', '.md'):
                return FileLoaderService._load_text_file(file_path)
            elif ext == '.docx':
                return FileLoaderService._load_docx_file(file_path)
            else:
                raise UnsupportedFileTypeError(f"File format '{ext}' is not supported. Please load .txt, .md, or .docx files.")
        except (FileNotFoundError, PermissionError, UnsupportedFileTypeError) as e:
            # Let specific errors propagate to be caught by the UI
            raise e
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {e}")
            raise FileLoadError(f"Failed to read the file: {str(e)}")

    @staticmethod
    def _load_text_file(file_path: str) -> str:
        """Reads a text-based file trying UTF-8-sig first, then UTF-16, and falling back to Latin-1."""
        # 1. Try UTF-8-sig (handles UTF-8 with or without BOM, stripping it automatically)
        try:
            with open(file_path, 'r', encoding='utf-8-sig', errors='strict') as f:
                return f.read()
        except UnicodeDecodeError:
            pass

        # 2. Try UTF-16
        try:
            with open(file_path, 'r', encoding='utf-16', errors='strict') as f:
                return f.read()
        except UnicodeDecodeError:
            pass

        # 3. Fallback to Latin-1 (never fails, guarantees decoding)
        logger.info(f"Encoding detection failed for {file_path}. Using Latin-1 fallback.")
        with open(file_path, 'r', encoding='latin-1') as f:
            return f.read()

    @staticmethod
    def _load_docx_file(file_path: str) -> str:
        """Extracts text content from paragraphs in a Microsoft Word document."""
        try:
            doc = Document(file_path)
            paragraphs = []
            for paragraph in doc.paragraphs:
                paragraphs.append(paragraph.text)
            return "\n".join(paragraphs)
        except Exception as e:
            logger.error(f"Docx loading failed: {e}")
            raise FileLoadError(f"Failed to extract text from Word document: {str(e)}")
