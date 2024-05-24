import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

slack_token = os.getenv("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

def post_answers_to_slack(channel, answers):
    try:
        # message = "Here are the answers to your questions:\n"
        # for question, answer in answers.items():
        #     message += f"\n*{question}*\n{answer}\n"
        
        response = client.chat_postMessage(
            channel=channel,
            text=answers
        )
        return response
    except SlackApiError as e:
        print(f"Error posting to Slack: {e.response['error']}")


# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError
# import os

# class SlackClient:
#     def __init__(self):
#         self.client = WebClient(token=os.getenv('SLACK_API_TOKEN'))

#     def post_message(self, channel, text):
#         try:
#             response = self.client.chat_postMessage(
#                 channel=channel,
#                 text=text
#             )
#         except SlackApiError as e:
#             print(f"Error posting message: {e.response['error']}")