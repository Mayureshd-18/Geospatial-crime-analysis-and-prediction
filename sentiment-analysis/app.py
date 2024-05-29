import pandas as pd
import numpy as np
import streamlit as st
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

# Initialize transformers
model_name = "deepset/roberta-base-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Define suspicious words and questions
suspicious_words = [
    "robbery", "crime", "exchange", "extortion", "threat", "suspicious", "fraud", "laundering",
    "illegal", "contraband", "smuggling", "burglary", "assault", "hijacking", "kidnapping", "ransom",
    "hostage", "terrorism", "homicide", "murder", "manslaughter", "weapon", "gun", "explosive", "bomb", "knives",
    "threaten", "blackmail", "intimidate", "menace", "harassment", "stalking", "kidnap", "abduction", "guns", "bombs",
    "abuse", "trafficking", "prostitution", "pimping", "drug", "narcotic", "cocaine", "heroin", "methamphetamine",
    "amphetamine", "opiate", "meth", "gang", "gangster", "mafia", "racket", "extort", "embezzle", "corruption",
    "bribe", "scam", "forgery", "counterfeit", "fraudulent", "cybercrime", "hacker", "phishing", "identity", "theft",
    "credit card", "fraud", "identity", "fraud", "ponzi", "scheme", "pyramid", "scheme", "money", "scam", "swindle", "deception",
    "conspiracy", "scheme", "plot", "coercion", "corrupt", "criminal", "felony", "misdemeanor", "felon", "fugitive",
    "wanted", "arson", "arsonist", "arsony", "stolen", "steal", "loot", "heist", "launder", "hitman", "racketeer",
    "hijack", "smuggle", "terrorist", "kidnapper", "perpetrator", "ringleader", "prowler", "vigilante", "sabotage",
    "saboteur", "suicide", "discreet", "hide", "action", "profile", "alert", "vigilant", "clandestine", "riot", "arms", "deal"
]

# Initialize Streamlit app
st.title("Crime Detection App")

# Load data
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
df = pd.read_excel(uploaded_file)
parsed_column = df['sentences'].to_list()

# Process sentences and store results
output_data = {'Crime Detected': [], 'Location Detected': [], 'Time Detected': []}

for sentence in parsed_column:
    answers = nlp({'question': "What event is going to take place?", 'context': sentence},
                  {'question': "Where is it going to happen", 'context': sentence},
                  {'question': "What time is it going to happen?", 'context': sentence})

    cw = set(answers[0]['answer'].lower().split()) & set(suspicious_words)

    if cw:
        output_data['Crime Detected'].append(answers[0]['answer'])
        output_data['Location Detected'].append(answers[1]['answer'] if answers[1]['answer'] else 'No location detected')
        output_data['Time Detected'].append(answers[2]['answer'] if answers[2]['answer'] else 'No time detected')
    else:
        output_data['Crime Detected'].append('No crime detected')
        output_data['Location Detected'].append('No location detected')
        output_data['Time Detected'].append('No time detected')

# Convert data to DataFrame
output_df = pd.DataFrame(output_data)

# Display results
st.write(output_df)

# Download button for Excel file
# st.download_button(label="Download Excel", data=output_df.to_excel(), file_name='crime_data_output.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
