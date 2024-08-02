import pdfplumber
import re
import nltk
from nltk.corpus import words as nltk_words

# Ensure NLTK data is downloaded
nltk.download('punkt')
nltk.download('words')

def is_valid_word(word):
    return word.lower() in nltk_words.words()

def clean_text(text):
    # Apply all cleaning steps to the text
    text = re.sub(r'(\w)-\s+(\w)', lambda match: match.group(1) + match.group(2) if is_valid_word(match.group(1) + match.group(2)) else match.group(0), text)
    
    text = re.sub(r'(\w)\s+(\w)', lambda match: match.group(1) + match.group(2) if is_valid_word(match.group(1) + match.group(2)) else match.group(0), text)
    
    text = re.sub(r'([a-z])\n([a-z])', r'\1 \2', text)
    
    text = re.sub(r'\s+', ' ', text)
    print(text)
    return text

def extract_and_clean_text_page_by_page(pdf_path):
    cleaned_text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            raw_text = page.extract_text()
            raw_text = raw_text.lower()
            if raw_text:  # Check if text extraction was successful
                cleaned_page_text = clean_text(raw_text)
                cleaned_text += cleaned_page_text + ' '  # Append cleaned text of each page
               


    return cleaned_text

# Assuming 'your_document.pdf' is your PDF file
cleaned_text = extract_and_clean_text_page_by_page('./data/SQ2_Cesspool_of_Redrook.pdf')
