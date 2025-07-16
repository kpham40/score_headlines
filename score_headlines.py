#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import os
from sentence_transformers import SentenceTransformer
from joblib import load
import numpy as np


# In[5]:


#!pip install joblib


# In[3]:


import os

# Load file from current working directory
print("Working directory:", os.getcwd())


# In[7]:


import argparse
import os
import sys
import datetime
import joblib
from sentence_transformers import SentenceTransformer

def load_headlines(file_path):
    """Read headlines from a text file, one per line."""
    if not os.path.exists(file_path):
        print(f" Error: The file '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        headlines = [line.strip() for line in f if line.strip()]
    
    if not headlines:
        print(f" Error: The file '{file_path}' is empty or contains only blank lines.")
        sys.exit(1)
    
    return headlines

def vectorize_headlines(headlines, model_name="all-MiniLM-L6-v2"):
    """Convert headlines to embeddings using SentenceTransformer."""
    model = SentenceTransformer(model_name)
    return model.encode(headlines)

def predict_labels(vectors, model_path="svm_headline_classifier.pkl"):
    """Load SVM model and predict labels for the input vectors."""
    if not os.path.exists(model_path):
        print(f" Error: Model file '{model_path}' not found.")
        sys.exit(1)

    model = joblib.load(model_path)
    return model.predict(vectors)

def write_results(predictions, headlines, source):
    """Write predictions and headlines to a dated output file."""
    today = datetime.datetime.now().strftime('%Y_%m_%d')
    output_filename = f"headline_scores_{source}_{today}.txt"

    with open(output_filename, 'w', encoding='utf-8') as f:
        for label, headline in zip(predictions, headlines):
            f.write(f"{label},{headline}\n")
    
    print(f" Output written to '{output_filename}'")

def main():
    parser = argparse.ArgumentParser(description="Classify news headlines as Optimistic, Pessimistic, or Neutral.")
    parser.add_argument("input_file", type=str, nargs="?", help="Text file with one headline per line.")
    parser.add_argument("source", type=str, nargs="?", help="Source of the headlines (e.g. 'nyt', 'chicagotribune').")

    args = parser.parse_args()

    # Check for required arguments
    if not args.input_file or not args.source:
        print("\n[❌] Missing required arguments.\n")
        print("Usage:")
        print("  python score_headlines.py <input_file> <source>\n")
        print("Example:")
        print("  python score_headlines.py todaysheadlines.txt nyt")
        print("  python score_headlines.py headlines_from_chicagotribune.txt chicagotribune\n")
        sys.exit(1)

    # Process headlines
    headlines = load_headlines(args.input_file)
    vectors = vectorize_headlines(headlines)
    predictions = predict_labels(vectors)
    write_results(predictions, headlines, args.source)

if __name__ == "__main__":
    main()

