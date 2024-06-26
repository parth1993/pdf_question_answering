import json

from dotenv import load_dotenv

from pdf_handler import extract_text_from_pdf
from qa_agent import OpenAILLM
from slack_client import post_answers_to_slack

load_dotenv()


def main(
    pdf_path: str, questions: list[str], slack_channel: str, embeddings_path: str = None
) -> None:
    text = None
    if not embeddings_path:
        text = extract_text_from_pdf(pdf_path)
    openai_llm = OpenAILLM()
    results = openai_llm.get_answers_from_text(
        questions=questions, text=text, path_to_embeddings=embeddings_path
    )
    json_blob = json.dumps(results, indent=2)
    post_answers_to_slack(slack_channel, f"```{json_blob}```")


if __name__ == "__main__":
    pdf_path = "./handbook.pdf"
    questions = [
        "What is the name of the company?",
        "Who is the CEO of the company?",
        "What is their vacation policy?",
        "What is the termination policy?",
    ]
    slack_channel = "#llms"
    embeddings_path = "./document_embedding.csv"
    main(pdf_path, questions, slack_channel, embeddings_path=embeddings_path)
