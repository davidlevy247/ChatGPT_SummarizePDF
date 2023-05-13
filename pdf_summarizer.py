import os
import openai
from PyPDF2 import PdfReader
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import re

# Set up OpenAI API key
openai.api_key = "your api key here"

def summarize_text(text):
    # Use OpenAI API to summarize text
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please review the text excerpt from a text book page and summarize into a few easy to understand parapgraphs, if the page does not contain anything you can summarize into a few easy to understand paragraphs then report why:\n\n{text}",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary = response.choices[0].text.strip()
    return summary

def is_text_suitable_for_summarization(text):
    # Check if the text contains at least some alphabetical characters
    return bool(re.search(r'[A-Za-z]+', text))

def main():
    # Open file selection dialog
    Tk().withdraw()
    pdf_file_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not pdf_file_path:
        print("No file selected. Exiting.")
        return

    # Read PDF file
    pdf_reader = PdfReader(pdf_file_path)

    # Create output text file with the same name as the source PDF
    input_file_name = os.path.splitext(os.path.basename(pdf_file_path))[0]
    output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{input_file_name}_summary.txt")

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        print("Starting summarization process...")
        for page_num, page in enumerate(pdf_reader.pages, start=1):
            print(f"Processing page {page_num}...")
            text = page.extract_text()
            
            if not text or not is_text_suitable_for_summarization(text):
                print(f"Page {page_num}: Unable to extract suitable text for summarization. Skipping.")
                output_file.write(f"Page {page_num}: Unable to extract suitable text for summarization. Skipping.\n\n")
                continue

            summary = None
            retries = 3
            while retries > 0:
                summary = summarize_text(text)
                if is_text_suitable_for_summarization(summary):
                    break
                retries -= 1

            if summary and is_text_suitable_for_summarization(summary):
                print(f"Page {page_num} summary: {summary}")
                output_file.write(f"Page {page_num} Summary:\n{summary}\n\n")
            else:
                print(f"Page {page_num}: Failed to generate a suitable summary.")
                output_file.write(f"Page {page_num}: Failed to generate a suitable summary.\n\n")
            
            output_file.flush()
            os.fsync(output_file.fileno())
            
        print("Summarization process completed.")

    print(f"Summarization complete. Results saved to: {output_file_path}")

if __name__ == "__main__":
    main()
