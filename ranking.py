import spacy
import requests
from collections import defaultdict

# Load the English NLP model
nlp = spacy.load("en_core_web_md")

# Example list of SPO triples, each represented as a tuple
spo_triples = [
    ('Python (programming language)', 'is used for', 'web development'),
    ('JavaScript', 'is used for', 'creating interactive web pages'),
    ('Machine learning', 'is a type of', 'artificial intelligence')
]

# Function to fetch and preprocess Wikipedia summary for a given topic
def preprocess_summary(topic):
    response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}")
    summary = ""
    if response.status_code == 200:
        data = response.json()
        summary = data['extract']
    doc = nlp(summary)
    # Extracting key phrases or named entities might represent the essence of the topic
    key_phrases = [chunk.text for chunk in doc.noun_chunks] + [ent.text for ent in doc.ents]
    return " ".join(key_phrases)

# Preprocess and analyze the triples
triples_info = defaultdict(dict)
for triple in spo_triples:
    subject, predicate, object_ = triple
    # Assuming the predicate's importance is in its relation, not in fetching its summary
    subject_info = preprocess_summary(subject)
    object_info = preprocess_summary(object_)
    triples_info[triple] = {"subject_info": subject_info, "object_info": object_info}

# Dummy ranking logic based on the length of processed info (for demonstration)
# In practice, you'd implement a more sophisticated ranking based on NLP analysis and graph centrality
sorted_triples = sorted(spo_triples, key=lambda x: len(triples_info[x]["subject_info"]) + len(triples_info[x]["object_info"]), reverse=True)

print("Ranked SPO Triples:")
for triple in sorted_triples:
    print(triple)