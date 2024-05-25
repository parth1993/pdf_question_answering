import ast

import pandas as pd
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI
from scipy import spatial

load_dotenv()

client = OpenAI()
BATCH_SIZE = 1000
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo-0125"


class OpenAILLM:

    def _generate_embeddings(self, texts: str) -> pd.DataFrame:
        embeddings = []
        for batch_start in range(0, len(texts), BATCH_SIZE):
            batch_end = batch_start + BATCH_SIZE
            batch = texts[batch_start:batch_end]
            print(f"Batch {batch_start} to {batch_end-1}")
            response = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
            for i, be in enumerate(response.data):
                assert (
                    i == be.index
                )  # double check embeddings are in same order as input
            batch_embeddings = [e.embedding for e in response.data]
            embeddings.extend(batch_embeddings)

        df = pd.DataFrame({"text": texts, "embedding": embeddings})
        return df

    def _strings_ranked_by_relatedness(
        self,
        query: str,
        df: pd.DataFrame,
        relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
        top_n: int = 100,
    ) -> tuple[list[str], list[float]]:
        """Returns a list of strings and relatednesses, sorted from most related to least."""
        query_embedding_response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=query,
        )
        query_embedding = query_embedding_response.data[0].embedding
        strings_and_relatednesses = [
            (row["text"], relatedness_fn(query_embedding, row["embedding"]))
            for i, row in df.iterrows()
        ]
        strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
        strings, relatednesses = zip(*strings_and_relatednesses)
        return strings[:top_n], relatednesses[:top_n]

    def _num_tokens(self, text: str, model: str = GPT_MODEL) -> int:
        """Return the number of tokens in a string."""
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))

    def _query_message(
        self, query: str, df: pd.DataFrame, model: str, token_budget: int
    ) -> str:
        """Return a message for GPT, with relevant source texts pulled from a dataframe."""
        strings, relatednesses = self._strings_ranked_by_relatedness(query, df)
        introduction = 'Use the below document on the company to answer the subsequent question. If the answer cannot be found in the articles, write "Data not available."'
        question = f"\n\nQuestion: {query}"
        message = introduction
        for string in strings:
            next_article = f'\n\nDocument section:\n"""\n{string}\n"""'
            if (
                self._num_tokens(message + next_article + question, model=model)
                > token_budget
            ):
                break
            else:
                message += next_article
        return message + question

    def _ask(
        self,
        query: str,
        df: pd.DataFrame,
        model: str = GPT_MODEL,
        token_budget: int = 4096 - 500,
        print_message: bool = False,
    ) -> str:
        """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
        message = self._query_message(query, df, model=model, token_budget=token_budget)
        if print_message:
            print(message)
        messages = [
            {"role": "system", "content": "Here are the answers to your questions:"},
            {"role": "user", "content": message},
        ]
        response = client.chat.completions.create(
            model=model, messages=messages, temperature=0
        )
        response_message = response.choices[0].message.content
        return response_message

    def get_answers_from_text(
        self,
        questions: list[str],
        text: str = None,
        path_to_embeddings: str = None,
    ) -> str:
        if not path_to_embeddings:
            df = self._generate_embeddings(texts=text)
        else:
            print(f"Loading embeddings from {path_to_embeddings}")
            df = pd.read_csv(path_to_embeddings)
            # convert embeddings from CSV str type back to list type
            df["embedding"] = df["embedding"].apply(ast.literal_eval)

        results = {}
        for question in questions:
            answer = self._ask(query=question.strip(), df=df)
            results[question] = answer
        return results
