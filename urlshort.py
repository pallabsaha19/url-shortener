from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
# jsonify package will help us to convert a python list/dictionary into json format
import json
import os.path

app = Flask(__name__)
# securely flash messages to the user, also to implement session we have to initialize a secret_key
app.secret_key = 'abarakadabra'

@app.route('/')
def index():
    # once a session has been setup we want a method to display the info to the user on home page
    return render_template('index.html', codes=session.keys())

# route by default use 'GET' method, therefore we have to explicitely specify that we want to use both
@app.route('/your-url',methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        # creating an empty dictionary to store the data which is entered in the form
        urls = {}

        ''' check if the value in the file already exists '''
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                # if the file exists then open the file
                urls = json.load(urls_file)

        # now check if the value already exists, then redirect to home page
        if request.form['code'] in urls.keys():

            ''' now we will flash message before returning '''
            flash('That short name has already been taken. Please use another name')
            return redirect(url_for('index'))

        ''' Now if the value is not there then this block of code will run '''
        # "go": {"url": "https://google.com"}
        urls[request.form['code']] = {'url':request.form['url']}
        # to create a json file
        with open('urls.json', 'w') as url_file:
            # now dump the data into the json file
            json.dump(urls,url_file)

            ''' implementing session after json file have got some data '''
            session[request.form['code']] = True       # initializing it to true means the session is activated

        # code=request.form['code'] is used to catch the short form of url entered by user in form and show it on 'your_url' web page
        return render_template('your_url.html', code=request.form['code'])

    else:
        # redirect func is used to redirect a user to a specific location (if anybody is tried using 'GET' method we will redirect them to home page
        return redirect(url_for('index'))



# making route for the short form entered by the user
# '/<short form entered by the user : where it is going to be saved>'
@app.route('/<string:code>')
def redirect_to_url(code):
    # check if the file exists, then load the json file
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            # if the value for the code is present
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])

    # if the file/code doesn't exist then we will return a 404 error
    return abort(404)


# for customized error pages we have to make route (when a user tries to enter wrong code in url)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# route for json API (if we show all the codes in home page then it will become messy, therefore we are adding new route so that user can see all codes from this end point
@app.route('/api')
def session_api():
    # return session keys from the session as a list and convert then into json format
    return jsonify(list(session.keys()))


app.run(debug=True)