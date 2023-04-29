from pdf2image import convert_from_path
import pytesseract
import util
import logging

from parser_prescription import PrescriptionParser
from parser_patient_details import PatientDetailsParser
from config import POPPLER_PATH, TESSERACT_CMD

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

logger = logging.getLogger(__name__)

def extract(file_path, file_format):
    # Step 1: Extracting text from PDF file
    pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)
    document_text = ''

    if len(pages) > 0:
        page = pages[0]
        processed_image = util.preprocess_image(page)
        text = pytesseract.image_to_string(processed_image, lang='eng')
        document_text = '\n' + text

    logger.debug(f'Text extracted from {file_format} document: {document_text}')

    # Step 2: Extract fields from text
    if file_format == 'prescription':
        extracted_data = PrescriptionParser(document_text).parse()
    elif file_format == 'patient_details':
        extracted_data = PatientDetailsParser(document_text).parse()
    else:
        raise Exception(f"Invalid document format: {file_format}")

    logger.debug(f'Data extracted from {file_format} document: {extracted_data}')

    return extracted_data

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    file_path = 'example.pdf'
    file_format = 'prescription'
    data = extract(file_path, file_format)
    logger.info(f'Data extracted from {file_path} ({file_format}): {data}')
