from answer import answer
from base_utils import base_utils
from halo import Halo
import json

def agent_1(query) : 

    spinner = Halo(
        text = f'Running Agent 1 ---> Reframing query {query}' , 
        spinner = 'dots')

    spinner.start()

    history = base_utils.get_history()

    prompt = open('Assets/prompt/agent_1/prompt.txt').read().format(history , query)

    response = answer.run_llm(prompt)

    open('Assets/prompt/agent_1/logs.txt' , 'w').write(
        f'''
        Original Query : {query}

        History : {history}

        Response : {response}
        ''')

    spinner.stop()

    return response

def agent_2(query , times_to_run = 2) : 

    spinner = Halo(
        text = f'Generating {times_to_run} for {query}' , 
        spinner = 'dots')

    spinner.start()

    prompt = open('Assets/prompt/agent_2/prompt.txt').read().format(times_to_run , query)

    response = answer.run_llm(prompt)

    open('Assets/prompt/agent_2/logs.txt' , 'w').write(
        f'''
        Original Query : {query}

        Times to run : {times_to_run}

        New Queries : {response}
        ''')

    questions = response.split('\n')

    spinner.stop()

    return questions

def agent_3(questions) : 

    spinner = Halo(
        text = f'Generating answers for {questions}' , 
        spinner = 'dots')

    spinner.start()

    answers = ''
    links = []

    for question in questions : 

        response , link = answer.answer_without_history(question)
            
        answers += response + '\n'

        links.append(link)


    # answers = '\n'.join([
    #     answer.answer_without_history(question)
    #     for question
    #     in questions
    # ])

    spinner.stop()

    open('Assets/prompt/agent_3/logs.txt' , 'w').write(
        f'''
        Questions : {questions}

        Answers : {answers}
        '''
    )

    return answers , links

def agent_4(n_response , query) : 

    spinner = Halo(
        text = f'Generating response for original query {query}' , 
        spinner = 'dots')

    spinner.start()

    response = answer.answer_with_history(query , n_response)

    spinner.stop()

    open('Assets/prompt/agent_4/logs.txt' , 'w').write(
        f'''
        N Response : {n_response}

        Original Query : {query}

        Response : {response}
        '''
    )

    return response

def run_agent(query) : 

    query = query['message']

    links = []

    if (
        'image' in query.lower() or 
        'images' in query.lower()
    ) : bot_response = {
        'image' : answer.get_images(query)
    }

    else : 

        reframed_query = agent_1(query)
        n_variation_questions = agent_2(reframed_query)
        n_answers , links = agent_3(n_variation_questions)
        main_response = agent_4(n_answers , query)

        open('Assets/Logs/chat_logs.json' , 'a').write(json.dumps({
            'query' : query , 
            'response' : main_response}) + '\n')

        bot_response = {
            'text' : main_response
        }

    return bot_response , links