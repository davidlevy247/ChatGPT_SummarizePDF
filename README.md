# ChatGPT_SummarizePDF

This Python script allows you to summarize pages from a PDF into a single text file, using the OpenAI API. 
Make sure the the PDF is correctly OCR converted before using, if there is text in images you want summarized.

The question prompt that ChatGPT will use to summarize each page is customizable during setup.
Additional settings for tweaking ChatGPT behavior is available within the python script.
Your API Key and Question prompt will be saved in a config.txt file next to the python script.
The script will ask you if you wish to encrypt the config.txt file or not.

## Prerequisites

- Python 3.8 or higher
- An API key from OpenAI. You can get it from here: [https://openai.com/](https://openai.com/)

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/davidlevy247/ChatGPT_SummarizePDF.git
    cd ChatGPT_SummarizePDF
    ```

2. Create a Python virtual environment and install the necessary packages. 

    - **Windows**:
        If the virtual environment folder doesn't exist, the provided `RunME.bat` script will create it, activate the virtual environment, and install the necessary packages. You can run it using:
        ```sh
        RunME.bat
        ```
    - **MacOS/Linux**:
        Run the following commands in the terminal:
        ```sh
        run.sh
        ```

3. You can rerun the script again as needed. 
    - **Windows**:
        ```sh
        RunME.bat
        ```
    - **MacOS/Linux**:
        ```sh
        run.sh
        ```
Please note:
If you get a freeze error in windows command prompt you can use Control+C to get command prompt back. If this happens make sure to open task manager processes and close the related python process which wil probably still be running if there is a command prompt freeze.

## Usage

The script will first check if a configuration file named `config.txt` exists. If it does not, it will ask for your OpenAI API key and a prompt. It will also ask you to provide a password for encryption if you decide you want to use ecryption. These details will be saved in the `config.txt` file in an encrypted form for later usage.

Once the initial setup is done, the script will open a file selection dialog where you can select the PDF file to summarize. After the summarization process is completed, a new text file containing the summaries of each page will be created in the same directory as the source PDF file.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
