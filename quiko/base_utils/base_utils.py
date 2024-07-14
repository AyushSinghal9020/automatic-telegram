from answer import answer
from datetime import datetime
import ast
import os

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

def predict_media_request(sentence):

  model = pickle.load(open('Assets/Models/media_request_model.pkl' , 'rb'))
  vectorizer = pickle.load(open('Assets/Models/media_request_vectorizer.pkl' , 'rb'))

  sentence_vector = vectorizer.transform([sentence])

  prediction = model.predict_proba(sentence_vector)[0][1]

  return prediction

def get_next_question_number() : 

    if not os.path.exists(r'Assets\Questions\question_counter.txt') :

        open(r'Assets\Questions\question_counter.txt' , 'w').write('1')

        number = 1

    else :

        number = int(open(r'Assets\Questions\question_counter.txt').read().strip())

        open(r'Assets\Questions\question_counter.txt' , 'w').write(str(number + 1))

    return number

def write_to_log(data) : 

    feedback = data.get('feedback')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    response = open('Assets/Logs/chat_logs.json').read().split("\n")[- 2]

    number = int(open('Assets/Questions/question_counter.txt').read().strip())

    log_entry = f'''
Number : {number}

Feedback [{timestamp}]: {feedback}

Response : {response}
    '''

    open('Assets/Feedback/feedback.txt' , 'a').write(f'{log_entry}\n\n')

def get_response_from_llm(data) : 

    user_message = data.get('message')

    question_number = get_next_question_number()

    if (
        'image' in user_message.lower() or 
        'images' in user_message.lower() or 
        'photos' in user_message.lower() or 
        'photo' in user_message.lower()) : 

        images = answer.get_images(user_message)

        bot_response = {'image' : images[0] if len(images) > 0 else ''}

        # bot_response = {
        #     'image' : [
        #         'https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Hydrochoeris_hydrochaeris_in_Brazil_in_Petr%C3%B3polis%2C_Rio_de_Janeiro%2C_Brazil_09.jpg/1200px-Hydrochoeris_hydrochaeris_in_Brazil_in_Petr%C3%B3polis%2C_Rio_de_Janeiro%2C_Brazil_09.jpg' , 
        #         'https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Hydrochoeris_hydrochaeris_in_Brazil_in_Petr%C3%B3polis%2C_Rio_de_Janeiro%2C_Brazil_09.jpg/1200px-Hydrochoeris_hydrochaeris_in_Brazil_in_Petr%C3%B3polis%2C_Rio_de_Janeiro%2C_Brazil_09.jpg'
        #     ]
        # }
    else : 

        response = answer.split_prompt_to_n(user_message , time_to_run = 5)

        bot_response = {'text' : response}

    return bot_response

def get_history() : return '\n'.join(open('Assets/Logs/chat_logs.json').read().split('\n')[- 6 :])