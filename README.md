# PDF Question Answering and Slack Notifier

## Overview
This project is an AI agent that extracts text from a PDF, answers a list of questions based on the content, and posts the results on Slack.

## Installation
1. Clone the repository.
2. Install the dependencies using `pip install -r requirements.txt`.
3. Set up your OpenAI API key and Slack bot token as environment variables.

## Usage
1. Update `main.py` with the path to your PDF file, your list of questions, and your Slack channel.
2. Run the main script using `python main.py`.

## Configuration
- OpenAI API key should be set as an environment variable `OPENAI_API_KEY`.
- Slack bot token should be set as an environment variable `SLACK_BOT_TOKEN`.