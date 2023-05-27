# -*- coding: utf-8 -*-
"""
Created on Sat May 27 20:32:23 2023

@author: willi
"""

import pandas as pd
import os
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

### SET DIRECTORIES

base_dir = os.path.dirname(os.path.abspath('__file__'))

tweets_df = pd.read_csv(base_dir + '/twitterdata/andrew_tate.csv')

persist_directory = base_dir + '/chromadb_hustlergpt_openai_dr'

### PROMPT TEMPLATE

prompt_template = """Use the following style and information examples to answer the question at the end. 
Rely on the examples predominantly.
Be very arrogant and aggressive. 
Always finish your response with the final sentence: "Hustlers must [verb]." where the verb follows from the answer.

{context}

Question: {question}
Answers:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

### STREAMLIT SESSION STATE
if 'openai_api_key' not in st.session_state:
    st.session_state['openai_api_key'] = 'you wish'


### STREAMLIT UI CODE

st.set_page_config(page_title="TopGPT", page_icon="🕶️", layout="wide")
st.title('TopGPT')
st.text('Ask HustlerBot anything 🕶️')
query = st.text_input('Write your question here!', value = ' ')

sendquery = st.button('ask!')

with st.sidebar:
    openai_api_key = st.text_input('put your OpenAI API key here and hit "enter"', key = 'openai_api_key')
    st.markdown('')
    st.markdown('')
    st.markdown('''
                **NOTE:** This app is a work of satire, built using all of Andrew Tate's tweets
                up to the 27th of May 2023. Any harmful outputs generated are a result
                of OpenAI's backend in combination with Andrew's own content, and
                DO NOT reflect the views and/or opinions of the developer.
                '''
                )
    
# if st.session_state['active']:
embeddings = OpenAIEmbeddings(openai_api_key = st.session_state['openai_api_key'])
if not os.path.exists(persist_directory + "/chroma-embeddings.parquet"):
    os.makedirs(persist_directory, exist_ok=True)
    texts = list(tweets_df.Tweets)
    docsearch = Chroma.from_texts(texts, 
                                  embeddings, ## Don't need this because results are worse with search by vector
                                  metadatas = [{'num_likes': \
                                                int(tweets_df.loc[i]['Number of Likes'])} \
                                                for i in tweets_df.index],
                                      persist_directory=persist_directory)
        
    docsearch.persist()
else:
    docsearch = Chroma(persist_directory = persist_directory, embedding_function = embeddings)
# else:
#     st.write('Put in your OpenAI API Key. Hustlers must click "activate".')

if sendquery:
    try:
        chain = load_qa_chain(OpenAI(temperature=1, openai_api_key = st.session_state['openai_api_key']), chain_type="stuff", prompt=PROMPT)
        if query.strip() != '' or query.strip() is not None or query.strip() != ['']:
            docs = docsearch.similarity_search(query, k= 5)
            answer = chain({"input_documents": docs, "question": query}, return_only_outputs=True)['output_text']
            st.markdown(answer)
        elif query.strip() == '' or query.strip() is None:
            st.write('You need to write words!')
        else:
            st.write('You need to write words!')
    except:
        st.write('Put your OpenAI API key into the sidebar and hit "Enter". Hustlers must sign up.')


        