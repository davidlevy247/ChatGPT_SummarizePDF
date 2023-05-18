import os
import openai
from PyPDF2 import PdfReader
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import re
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import getpass
from datetime import datetime
import sys
from colorama import Fore, Style

CONFIG_FILE = 'config.txt'

def get_encryption_key():
    password = getpass.getpass("Enter your password: ").encode()  # Get the password for encryption
    salt = b'\x00'*16  # Just for simplicity we use static salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password))

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(data, key):
    f = Fernet(key)
    return f.decrypt(data)

def load_config(config_file, encryption_key=None):
    if os.path.exists(config_file):
        with open(config_file, 'rb') as f:
            data = f.read()
        if encryption_key is not None:
            try:
                data = decrypt_data(data, encryption_key)
            except:
                return None, None
        return data.decode().split('\n')

    return None, None

def save_config(config_file, api_key, prompt, encryption_key=None):
    data = f"{api_key}\n{prompt}"
    if encryption_key is not None:
        data = encrypt_data(data.encode(), encryption_key)
    else:
        data = data.encode()
    with open(config_file, 'wb') as f:
        f.write(data)

if os.path.exists(CONFIG_FILE):
    attempts = 3
    while attempts > 0:
        encryption_key = get_encryption_key()
        api_key, prompt = load_config(CONFIG_FILE, encryption_key)
        
        if api_key is not None and prompt is not None:
            break  # Successful decryption

        print(f"{Fore.RED}Incorrect password.{Style.RESET_ALL} {Fore.GREEN}Remaining Attempts:{Style.RESET_ALL} {Fore.RED}{attempts-1}{Style.RESET_ALL}")
        attempts -= 1

    if attempts == 0:
        if input(f"{Fore.RED}Unable to decrypt the configuration file.{Style.RESET_ALL} {Fore.GREEN}Would you like to create a new one?{Style.RESET_ALL} [y/N]: ").strip().lower() in ['y', 'yes']:
            api_key = input(f"{Fore.GREEN}Enter your OpenAI API key: {Style.RESET_ALL}")
            sys.stdout.write(Fore.RED + "Enter your prompt to ask ChatGPT for your desired results per page. " + Style.RESET_ALL)
            sys.stdout.write("For example, 'Please summarize the following single page from a PDF book into coherent easy to understand paragraphs without indentations or early line breaks; sometimes a single page may be impossible to summarize into one to three paragraphs, so when that happens report what the problem is with the page:'\n")
            prompt = input(f"{Fore.GREEN}Enter your prompt: {Style.RESET_ALL}")
            use_encryption = input(f"{Fore.GREEN}Would you like to use encryption for the config file?{Style.RESET_ALL} [y/N]: ").strip().lower() in ['y', 'yes']
            encryption_key = get_encryption_key() if use_encryption else None
        else:
            print("Exiting program.")
            exit(1)

    else:  # Proceed with the existing decrypted config
        if input(f"{Fore.GREEN}Would you like to change the API key?{Style.RESET_ALL} [y/N]: ").strip().lower() in ['y', 'yes']:
            api_key = input("{Fore.GREEN}Enter your new OpenAI API key:{Style.RESET_ALL} ")
        if input(f"{Fore.GREEN}Would you like to change the prompt? Current prompt:{Style.RESET_ALL} '{prompt}' [y/N]: ").strip().lower() in ['y', 'yes']:
            sys.stdout.write(Fore.RED + "Your prompt to ask ChatGPT for your desired results per page should be carefully written. " + Style.RESET_ALL)
            sys.stdout.write("For example, 'Please summarize the following single page from a PDF book into coherent easy to understand paragraphs without indentations or early line breaks; sometimes a single page may be impossible to summarize into one to three paragraphs, so when that happens report what the problem is with the page:'\n")
            prompt = input(f"{Fore.GREEN}Enter your prompt: {Style.RESET_ALL}")
        if input(f"{Fore.GREEN}Would you like to change the encryption status of the config file?{Style.RESET_ALL} [y/N]: ").strip().lower() in ['y', 'yes']:
            use_encryption = input(f"{Fore.GREEN}Would you like to use encryption for the config file?{Style.RESET_ALL} [y/N]: ").strip().lower() in ['y', 'yes']
            encryption_key = get_encryption_key() if use_encryption else None

    os.rename(CONFIG_FILE, f"{CONFIG_FILE}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak")
else:  # config.txt does not exist
    sys.stdout.write(Fore.GREEN + "No configuration file found. Let's create a new one."  + Style.RESET_ALL + "\n")
    api_key = input("Enter your OpenAI API key: ")
    sys.stdout.write(Fore.RED + "Enter your prompt to ask ChatGPT for your desired results per page. " + Style.RESET_ALL)
    sys.stdout.write("For example, 'Please summarize the following single page from a PDF book into coherent easy to understand paragraphs without indentations or early line breaks; sometimes a single page may be impossible to summarize into one to three paragraphs, so when that happens report what the problem is with the page:'\n")
    prompt = input(f"{Fore.GREEN}Enter your prompt: {Style.RESET_ALL}")
    use_encryption = input(f"{Fore.GREEN}Would you like to use encryption for the config file?{Style.RESET_ALL} [y/N]: ").strip().lower() in ['y', 'yes']
    encryption_key = get_encryption_key() if use_encryption else None

# Save new configuration
save_config(CONFIG_FILE, api_key, prompt, encryption_key)

# Set up OpenAI API key
openai.api_key = api_key

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
	
    # Get total number of pages
    total_pages = len(pdf_reader.pages)

    # Create output text file with the same name as the source PDF
    input_file_name = os.path.splitext(os.path.basename(pdf_file_path))[0]
    output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{input_file_name}_summary.txt")

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        print("Starting summarization process...")
        for page_num, page in enumerate(pdf_reader.pages, start=1):
			# Show the page currently being processed and the total number of pages
            print(f"{Fore.GREEN}Processing page {page_num} of {total_pages}...{Style.RESET_ALL}")
            text = page.extract_text()
            
            if not text or not is_text_suitable_for_summarization(text):
                print(f"{Fore.RED}Page {page_num}: Unable to extract suitable text for summarization. Skipping.{Style.RESET_ALL}")
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
