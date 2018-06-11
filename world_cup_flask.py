import json
from flask import Flask,render_template_string,request,render_template
from scoring import match_handle, compute_idf
app = Flask(__name__)

compute_idf()
vects = pickle.load (open ("pickle/some_file_name", "rb"))

@app.route('/')
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

app.run()
