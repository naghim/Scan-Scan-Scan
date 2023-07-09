# Scan Scan Scan!

This program allows users to automate scanning tasks using voice recognition.

By simply saying "Scan" or "Print", the program will automatically initiate the scanning process for the next page.

It can also detect words that are similar to "Scan", accounting for various accents.

## Prerequisites

Before running this program, ensure that you have the following dependencies installed:

- [Not Another PDF Scanner 2](https://naps2.com)
- Python 3.11+
- Python libraries:
  - Please install dependencies using pip: `python -m pip install -r requirements.txt`
- Vosk speech recognition models:
  - Please download the model from [GitHub](https://github.com/alphacep/vosk-api/blob/master/doc/models.md) and unpack into a folder called `model` in the current directory

## Usage

Basic usage example:

```bash
python scan.py --x 40 --y 70 --window-title "Not Another PDF Scanner 2"
```

This will click the "Not Another PDF Scanner 2" application on the (40, 70) mouse position every time you say "Scan" through the microphone.

This program was made in mind for the "Not Another PDF Scanner 2" application, though through trial and error the arguments can be changed to accomodate another program.
