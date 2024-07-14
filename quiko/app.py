import os

from upload import upload
from process import process
from base_utils import base_utils
from datetime import datetime
from agents import agents

from flask import Flask , render_template , request , redirect , url_for , session , flash , jsonify

os.environ['OPENAI_API_KEY'] = 'sk-proj-akdeZO2k0thnW5qqSQPiT3BlbkFJFVW45H5G0FVUuzST2rLo'

def log_login_attempt(username , success) : 

    with open('loginlogs.txt' , 'a') as f : 

        log_entry = f"{datetime.now()} - {'Success' if success else 'Failure'} - User: {username}\n"
        f.write(log_entry)

app = Flask(__name__)
app.secret_key = 'lohitchat'
open('chat_logs.json' , 'w').write('')

# Static user credentials
users = {
    'user1@gmail.com': 'user1@123',
    'user2@gmail.com': 'user2@123',
    'amit@blubirch.com':'amit@123',
    'boschuser@gmail.com':'123456',
    'boschuser2@gmail.com':'123456',
    'wealthyuser@gmail.com':'123456',
    'wealthyuser2@gmail.com':'123456',
    'algonomyuser@gmail.com':'123456',
    'algonomyuser2@gmail.com':'123456'
}


@app.route('/')
def home() : return redirect(url_for('login'))

@app.route('/discovery')
def discovery_upload_page() : return render_template('discovery.html')

@app.route('/upload')
def main_upload_page() : return render_template('admin.html')

@app.route('/login' , methods = ['GET' , 'POST'])
def login() : 

    if request.method == 'POST' : 

        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password :

            if username == 'boschuser@gmail.com' or username == 'boschuser2@gmail.com' : return redirect(f"http://bosch.copilotgtm.com/directlogin?username={username}&password={password}")
            if username == 'wealthyuser@gmail.com' or username == 'wealthyuser2@gmail.com' : return redirect(f"http://wealthy.copilotgtm.com/directlogin?username={username}&password={password}")
            if username == 'algonomyuser@gmail.com' or username == 'algonomyuser2@gmail.com' : return redirect(f"http://algonomy.copilotgtm.com/directlogin?username={username}&password={password}")

            session['username'] = username
            log_login_attempt(username , True)

            return redirect(url_for('dashboard'))

        else : 
       
            log_login_attempt(username , False)
            flash('Invalid username or password')

    return render_template('login.html')



@app.route('/dashboard')
def dashboard() : 

    if 'username' in session : return render_template('index.html' , username = session['username'])
    else : return redirect(url_for('login'))

@app.route('/discovery/upload' , methods = ['POST'])
def discovery_upload_file() : 

    file = request.files

    if 'file' not in file: return jsonify({'error': 'No file part in the request'}), 400

    file = file['file']

    response = upload.upload(file , end_point = 'discovery')

    return response

@app.route('/api/feedback' , methods = ['POST'])
def feedback() : 

    data = request.json

    base_utils.write_to_log(data)

    return jsonify({'status': 'Feedback received'})


@app.route('/api/chatbot' , methods = ['POST'])
def chatbot() : 

    data = request.get_json()

    bot_response , links = agents.run_agent(data)
    # # bot_response = { 
    # #     'text' : "orem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum"
    # # }
    # bot_response = {
    #     'image' : [
    #         'https://cdn.pixabay.com/photo/2023/08/02/18/21/yoga-8165759_640.jpg' , 
    #         'https://cdn.pixabay.com/photo/2023/08/02/18/21/yoga-8165759_640.jpg' , 
    #         'https://cdn.pixabay.com/photo/2023/08/02/18/21/yoga-8165759_640.jpg'
    #     ] 
    # }

    unique_links = []

    for link in links :

        if link not in unique_links : unique_links.append(link)

    for link in unique_links : 

        if 'text' in bot_response : bot_response['text'] += f'\n\n{link}'

    return jsonify(response = bot_response)


@app.route('/api/upload' , methods = ['POST'])
def upload_file() : 

    file = request.files

    if 'file' not in file: return jsonify({'error': 'No file part in the request'}), 400

    file = file['file']

    response = upload.upload_s3(file)

    return response


@app.route('/api/process' , methods = ['POST'])
def process_file() : 

    response = process.process()

    return jsonify({'message': 'Processing completed successfully.'}), 200


@app.route('/logout')
def logout() : 

    session.pop('username' , None)

    return redirect(url_for('login'))


# if __name__ == '__main__' : app.run(host = '0.0.0.0', port = 5000 , debug = True , use_reloader = False)
#if __name__ == '__main__' : app.run(host = '0.0.0.0', port = 5000 , debug = True , use_reloader = True)
if __name__ == '__main__' : app.run(host = '0.0.0.0', port = 5008 , debug = True , use_reloader = True)