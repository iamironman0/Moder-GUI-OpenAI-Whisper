# OpenAI Whisper Audio Transcriber
	
This is a simple GUI application that transcribes audio files using OpenAI Whisper. The app is built using Python and customtkinter.

## Preview
![preview](https://user-images.githubusercontent.com/63475761/224495737-d7dd2398-b732-4751-bd4f-60e5c5fbefc1.png)

## Features
* Models: Tiny, Base, Small, Medium, Large
* Languages: Arabic, English
* Task: Transcribe, Translate
* Save transcription results to a text file
* Change appearnce mode

## Setup

### Requirements
* Python version 3.9
* Torch with Cuda
* Nvidia GPU
* ffmpeg
* customtkinter 

> For more information please visit OpenAI Wishper github: https://github.com/openai/whisper

1. Install the required dependencies by running the following command:

```
pip install -r requirements.txt
```
On macOS and Linux, use pip3 instead:
```
pip3 install -r requirements.txt
```

2. Run the application by executing the following command:

```
python main.py 
```
On macOS and Linux, use python3 instead:

```
python3 main.py
