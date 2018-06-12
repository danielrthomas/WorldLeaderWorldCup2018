import json
import pickle
from flask import Flask,render_template_string,request,render_template
from scoring import match_handle, compute_idf
app = Flask(__name__)

compute_idf()
try:
    vects = pickle.load (open ("/home/infolab/apps/WorldCup/app/pickle/some_file_name", "rb"))
except:
    vects = pickle.load (open ("pickle/some_file_name", "rb"))

def main():
    handle = request.args.get('handle')
    if handle == None or handle == '':
        #get username
        return render_template('input_handle.html')
    else:
        #we have username, now compute the scores and return
        try:
            ranking = match_handle(handle,vects)
        except:
            ranking = []
        return render_template('result.html',rank=ranking)

@app.route('/contact')
def contact():
    return render_template('contact.html')

#app.run()
if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)
