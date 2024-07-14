import os 
import json
import PyPDF2

from langchain.schema.document import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.openai import OpenAIEmbeddings
from halo import Halo
import boto3
from tqdm import tqdm

def get_client() : 

    s3 = boto3.client(
        's3' , 
        aws_access_key_id = 'AKIA6ODUZOOJMU43F36V' , 
        aws_secret_access_key = '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'
    )

    return s3

def pdf_to_documets(pdf_path) : 

    pdf_name = pdf_path.split('/')[-1]
    pdf = PyPDF2.PdfReader(pdf_path)

    documents = []

    for page_number in range(len(pdf.pages)) : 

        text = pdf.pages[page_number].extract_text()

        chunks = [
            text[index : index + 1024]
            for index 
            in range(0 , len(text) , 1024)
        ]

        for chunk in chunks :

            documents.append(
                Document(
                    page_content = chunk , 
                    metadata = {
                        'source_type' : 'pdf' , 
                        'source_name' : pdf_path , 
                        'iter_number' : page_number , 
                        'type' : 'pdf' , 
                        'url' : f'https://blubirch-pdf.s3.amazonaws.com/{pdf_name}'    
                    }
                ))

    return documents

def json_to_documents(json_path) : 

    documents = []

    for doc in json.load(open(json_path)) : 

        documents.append(Document(
            page_content = doc['page_content'] , 
            metadata = {
                'source_type' : 'json' , 
                'source_name' : json_path ,
                'iter_number' : 0 ,
                'type' : doc['type'] , 
                'url' : doc['url']
            }
        ))

    return documents 

def process() : 

    s3 = get_client()

    text_documents = []
    image_documents = []

    page_iterator = s3.get_paginator('list_objects_v2')
    page_iterator = page_iterator.paginate(Bucket = 'blubirch-pdf')

    for page in page_iterator : 

        if 'Contents' in page : 

            for obj in tqdm(page['Contents'] , total = len(page['Contents'])) : 

                key = obj['Key']

                if key.endswith('json') or key.endswith('pdf') : 

                    try : 
                        

                        s3.download_file('blubirch-pdf' , key , 'Assets/uploads/main/' + key)
                        if key.endswith('json') : image_documents += json_to_documents('Assets/uploads/main/' + key)
                        if key.endswith('pdf') : text_documents += pdf_to_documets('Assets/uploads/main/' + key)

                        os.remove('Assets/uploads/main/' + key)

                    except : pass

    if len(text_documents) != 0 : 

        spinner = Halo(text = 'Creating text vector store' , spinner = 'dots')
        spinner.start()

        text_vc = FAISS.from_documents(
            text_documents ,
            embedding = OpenAIEmbeddings(model="text-embedding-3-large"))

        text_vc.save_local('Assets/vectorstore/text_vc')

        spinner.stop()

    if len(image_documents) != 0 :

        spinner = Halo(text = 'Creating image vector store' , spinner = 'dots')
        spinner.start()

        image_vc = FAISS.from_documents(
            image_documents ,
            embedding = OpenAIEmbeddings(model="text-embedding-3-large"))

        image_vc.save_local('Assets/vectorstore/img_vc')

        spinner.stop()