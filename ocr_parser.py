import pdfplumber
from PIL import Image
import pytesseract
import io

class OCRParser:
    def __init__(self, tesseract_cmd_path=None):
        if tesseract_cmd_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        images = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                    # Extract images if present
                    for img in page.images:
                        if 'stream' in img:
                            image = Image.open(io.BytesIO(img['stream'].get_data()))
                            images.append(image)
        except Exception as e:
            print(f"Error extracting text/images from PDF {pdf_path}: {e}")
        return text, images

    def extract_text_from_image(self, image_path):
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error extracting text from image {image_path}: {e}")
            return ""

# Example Usage:
# from config import Config
# ocr_parser = OCRParser(Config.TESSERACT_CMD)
# text, images = ocr_parser.extract_text_from_pdf("data/raw_appraisals/sample_report.pdf")
# print("Extracted Text:", text[:200])