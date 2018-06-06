import json
from flask import Flask,render_template_string,request,render_template
app = Flask(__name__)                         

@app.route('/')
def input_handle():
    handle = request.args.get('handle')
    if handle == None or handle == '':
        #get username
        print 'here'
        return render_template('input_handle.html')
    else:
        pass
        #we have username, now compute the scores and return 
app.run()
