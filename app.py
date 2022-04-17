from flask import Flask, request, jsonify
from secrets import token_urlsafe
from config import HOST_URL, HOST_PORT
from app_manager import *

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Encurtador de URL</p>"

    
@app.route("/<token>", methods=['GET'])
def acess_page(token):
    confirmation = check_token(token)
    if confirmation == True:
        page = go_to_the_page(token)
    else:
        page = '<h1>Essa página não existe</h1>' #TODO: Fazer uma página
    
    return page

@app.route('/create',methods=["POST"])
def register_new_url():
    response = request.get_json()
    url = response['url']
    token = token_urlsafe(8)
    register_url(url, token)
    short_url = f'http://{HOST_URL}:{HOST_PORT}/{token}'
    return jsonify(new_url=short_url)

@app.route('/list', methods=['GET'])
def list_all_urls():
    response = get_all_urls()
    return jsonify(response)

@app.route('/delete/<token>', methods=['POST']) 
def delete_url(token):
    confirmation = check_token(token)
    if confirmation == True:
        message = delete_url_database(token)
        return jsonify(message='This url is delete from database')

    else:
        return'<h1>Essa página não existe</h1>' #TODO: Fazer uma página



    
   
if __name__ == '__main__':
    app.run(host=HOST_URL, port=HOST_PORT, debug=True)
