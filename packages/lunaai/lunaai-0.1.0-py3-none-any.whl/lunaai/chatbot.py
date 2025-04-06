"""
LunaAI - A Retrieval-Based QnA and Code Generation Chatbot
Author: Joydeep Dutta

This module defines a chatbot system that uses sentence-transformer embeddings,
cosine similarity, and fuzzy matching to answer queries based on a custom dataset.
"""

import gdown
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from rapidfuzz import process, fuzz
import os
import csv


class _LoadResources:
    """Handles loading of embedding files and CSV datasets."""
    def __init__(self):
        self._embeddings_npy = None
        self._chunk_datasets = None

    def load_embeddings_file(self, url: str, model_name: str):
        """Downloads and loads the embedding NumPy file."""
        output = f"embeddings_file_{model_name}.npy"
        if os.path.exists(output):
            self._embeddings_npy = np.load(output, allow_pickle=True)
            return self._embeddings_npy

        gdown.download(f"https://drive.google.com/uc?id={url}", output, quiet=False)
        self._embeddings_npy = np.load(output, allow_pickle=True)
        return self._embeddings_npy

    def load_csv_dataset(self, url: str):
        """Downloads and loads the CSV dataset as a DataFrame."""
        url = f"https://drive.google.com/uc?id={url}"
        self._chunk_datasets = pd.read_csv(url, encoding='utf-8', on_bad_lines='skip')
        return self._chunk_datasets


class LunaAI:
    """Main chatbot class for query-response using embedding similarity."""
    def __init__(self, api: str, accuracy: float = 0.6, fuzzy_threshold: int = 70,
                 sentence_model: str = 'paraphrase-MiniLM-L3-v2'):
        """
        Initializes the chatbot with configuration.

        Parameters:
        - api: str -> Google Drive API keys (CSV+Model+Numpy IDs)
        - accuracy: float -> Cosine similarity threshold
        - fuzzy_threshold: int -> Fuzzy match score threshold (0-100)
        - sentence_model: str -> Name of the sentence-transformers model
        """
        self._display_slowly("Just a sec . . .")
        self._st_model = SentenceTransformer(sentence_model)
        self._API_KEY = api
        self._accuracy = accuracy
        self._fuzzy_threshold = fuzzy_threshold
        self._load_data()

    def _load_data(self):
        """Loads CSV and embedding data using the API key."""
        obj = _LoadResources()
        keys = self._API_KEY.split("+")
        luna_csv = keys[0]
        model_name = keys[1]
        luna_npy = keys[2]

        self._display_slowly(f"Selected model : {model_name}")
        self._dataframe = obj.load_csv_dataset(url=luna_csv)
        self._prompts = self._dataframe['Prompt'].astype(str).tolist()
        self._responses = self._dataframe['Response'].astype(str).tolist()
        self._prompt_embeddings = obj.load_embeddings_file(url=luna_npy, model_name=model_name)

    def get_response(self, user_query: str):
        """Returns the best response for a user query using cosine and fuzzy matching."""
        if not self._prompts:
            return None

        processed_query = self._extract_keywords(user_query)
        query_embedding = self._st_model.encode([processed_query])
        similarities = cosine_similarity(query_embedding, self._prompt_embeddings)
        best_match_idx = similarities.argmax()
        best_match_score = similarities[0][best_match_idx]

        if best_match_score > self._accuracy:
            return self._responses[best_match_idx], best_match_score

        fuzzy_match, fuzzy_score, _ = process.extractOne(processed_query, self._prompts, scorer=fuzz.partial_ratio)
        if fuzzy_score >= self._fuzzy_threshold:
            best_fuzzy_idx = self._prompts.index(fuzzy_match)
            return self._responses[best_fuzzy_idx], fuzzy_score / 100

        return "I don't have answer for that now!", best_match_score

    def _extract_keywords(self, text: str):
        """Extracts keywords by removing stopwords from a query."""
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words("english"))
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
        return " ".join(set(filtered_tokens))

    def _display_slowly(self, text: str, delay: float = 0.055):
        """Prints characters of a string one by one with delay."""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()


def save_to_csv(prompt: str, response: str, feedback: str, filename: str = 'feedback.csv'):
    """Appends feedback entry to a CSV file."""
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Prompt', 'Response', 'Feedback'])
        writer.writerow([prompt, response, feedback])


def chat(api_key: str):
    """Main CLI interface for the chatbot."""
    try:
        chatbot = LunaAI(api=api_key)
    except Exception as e:
        print(e)
        return

    while True:
        inp = input("Enter your query : ").lower()
        if inp in ['bye', 'exit', 'goodbye']:
            chatbot._display_slowly("Goodbye! Feel free to reach out!")
            break
        response, confidence = chatbot.get_response(inp)
        whole_response = f"{response} ({confidence:.2f})"
        chatbot._display_slowly(whole_response)
        feedback = input("Was that correct? ")
        save_to_csv(inp, response, feedback)

 