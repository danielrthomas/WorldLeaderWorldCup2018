import json
from flask import Flask,render_template_string,request,render_template
app = Flask(__name__)                         

@app.route('/')
def main():
    handle = request.args.get('handle')
    if handle == None or handle == '':
        #get username
        return render_template('input_handle.html')
    else:
        #we have username, now compute the scores and return
        ranking = [[25,'Country','realDonaldTrump',['nasty','woman','im','with','her']]]
        return render_template('result.html',rank=ranking)

    
app.run()
