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

For windows users, before proceeding, ensure that Python and Pip are added to your environment variables. This can be confirmed by running `python --version` and `pip --version` from the command prompt. If both commands return a version number, Python is set up correctly. If not, please refer to the section 'Setting up Python Path on Windows' below.

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

## Setting up Python Path on Windows

If the Python command is not recognized in the command prompt, it's likely that Python is not added to your PATH environment variable. This can be done as follows:

1. Locate your Python installation. Typically, it's in the `C:\Users\YourUserName\AppData\Local\Programs\Python\PythonVersion\` folder. Note: I habitually avoid installing programs on my OS drive, you can have python installed in a custom directory and on a different drive.
2. Copy the path to the Python installation directory.
3. Open the Start Menu and search for 'Environment Variables'. Click on 'Edit the system environment variables'.
4. In the System Properties window that appears, click on 'Environment Variables'.
5. In the Environment Variables window, under the 'System variables' section, find and select the 'Path' variable, then click on 'Edit'.
6. In the Edit Environment Variable window, click on 'New', then paste the path to your Python installation directory. Do the same for the 'Scripts' subdirectory inside your Python installation directory.
7. Click 'OK' in all windows to save your changes.

Remember to open a new command prompt window to see the changes.

## Usage

The script will first check if a configuration file named `config.txt` exists. If it does not, it will ask for your OpenAI API key and a prompt. It will also ask you to provide a password for encryption if you decide you want to use ecryption. These details will be saved in the `config.txt` file in an encrypted form for later usage.

Once the initial setup is done, the script will open a file selection dialog where you can select the PDF file to summarize. After the summarization process is completed, a new text file containing the summaries of each page will be created in the same directory as the source PDF file.

Please note: The quality of the generated summary highly depends on the content of the PDF file and the quality of the OCR conversion if it was required. The script might not always generate a suitable summary due to these factors.

## Troubleshooting

- If you encounter any errors during the installation or the run process, try to carefully read the error message. It often provides clues about what went wrong.
- If you get a freeze error in the Windows command prompt, you can use Control+C to get the command prompt back. However, make sure to open the Task Manager and close the related Python process which will probably still be running.
- If you encounter issues related to the OpenAI API, ensure that you have correctly entered your API key, and that your key has the necessary permissions and hasn't exceeded any rate limits.

## Contribution

Your contributions are always welcome! If you have suggestions for improvements or encounter a bug, please open an issue. Or, you can improve this project by opening a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
