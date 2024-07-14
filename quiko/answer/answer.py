import json

from halo import Halo
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from base_utils import base_utils
from groq import Groq

def run_llm(prompt) : 

    client = Groq(api_key = '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')

    chat_completion = client.chat.completions.create(
        messages = [
            {
                'role' : 'user' , 
                'content' : prompt
            }
        ] , model = 'llama3-80b-8192'
    )

    response = chat_completion.choices[0].message.content

    return response

def run_llm(prompt) :

    client = OpenAI()

    stream = client.chat.completions.create(
        model = 'gpt-4o' ,
        messages = [
            {
                'role' : 'user' , 
                'content' : prompt}] , 
        stream = True)
    response = ''

    for chunk in stream : 

        if chunk.choices[0].delta.content : response += chunk.choices[0].delta.content

    return response


def get_images(query) : 

    vc = FAISS.load_local(
        'Assets/vectorstore/img_vc' ,
        embeddings = OpenAIEmbeddings(model = 'text-embedding-3-large') ,  
        allow_dangerous_deserialization = True) 

    similar_docs = vc.similarity_search(query)

    images = [doc.metadata['url'] for doc in similar_docs if doc.metadata['type'] == 'image']

    return images

def answer_without_history(query) : 

    vc = FAISS.load_local(
        'Assets/vectorstore/text_vc' ,
        embeddings = OpenAIEmbeddings(model = 'text-embedding-3-large') ,  
        allow_dangerous_deserialization = True
    ) 

    similar_docs = vc.similarity_search(query)

    context = ' '
    links = []

    for doc in similar_docs : 

        context += f'''
        Page Content : {doc.page_content}

        source_type : {doc.metadata['source_type']}

        source_name : {doc.metadata['source_name']}

        iter_number : {doc.metadata['iter_number']}        
        '''

        links.append(doc.metadata['url'])

    prompt = open('Assets/prompt/agent_3/prompt.txt').read().format(context , query)

    response = run_llm(prompt)

    return response , links

def answer_with_history(query , n_response) : 

    print(query)

    # vc = FAISS.load_local(
    #     'Assets/vectorstore/text_vc' ,
    #     embeddings = OpenAIEmbeddings(model = 'text-embedding-3-large') ,  
    #     allow_dangerous_deserialization = True
    # ) 

    # similar_docs = vc.similarity_search(query)

    # context = ' '

    # for doc in similar_docs : 

    #     context += f'''
    #     Page Content : {doc.page_content}

    #     source_type : {doc.metadata['source_type']}

    #     source_name : {doc.metadata['source_name']}

    #     iter_number : {doc.metadata['iter_number']}        
    #     '''

    history = base_utils.get_history()

    prompt = open('Assets/prompt/agent_4/prompt.txt').read().format(n_response , history , query)

    response = run_llm(prompt)

    return response