import os

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

slack_token = os.getenv("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)


def post_answers_to_slack(channel, answers):
    try:
        # message = "Here are the answers to your questions:\n"
        # for question, answer in answers.items():
        #     message += f"\n*{question}*\n{answer}\n"

        response = client.chat_postMessage(channel=channel, text=answers)
        return response
    except SlackApiError as e:
        print(f"Error posting to Slack: {e.response['error']}")
