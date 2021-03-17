from flask import Flask, request, make_response, url_for, redirect, flash, render_template, session, jsonify
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
import authomatic
import logging

from services.databaseService import DatabaseService
from services.userService import UserService
from services.recordService import RecordService
from services.jwtService import JWTService

from config import CONFIG

# Instantiate Authomatic.
authomatic = Authomatic(CONFIG, 'AnderG3h3impi3Hi3rzo!', report_errors=False)

app = Flask(__name__, template_folder='html')
app.config['SECRET_KEY'] = 'Sup3rgeheimhee!'

db = DatabaseService()
userService = UserService(db)
recordService = RecordService(db)
jwtService = JWTService()

@app.route('/')
def index():
    user = None
    print('sesion...', session)
    if (session.get('googleId') != None):
        user = userService.getByGoogleId(session.get('googleId'))
        userRecors = recordService
        print(user)

    return render_template('index.html', user=user)

@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    response = make_response()
    result = authomatic.login(
        WerkzeugAdapter(request, response),
        provider_name,
        session=session,
        session_saver=lambda: app.save_session(session, response)
    )

    print(session)

    if result:
        print('result', result)
        if result.user:
            result.user.update()
            user = userService.getByGoogleId(result.user.id)
            if user == None:
                user = userService.create({
                    'email': result.user.email,
                    'name': result.user.name,
                    'googleId': result.user.id,
                })
            print('user ID = ', user['_id'])
            token = jwtService.encode(user['_id'])
            session['token'] = token

            return redirect('/')

        return render_template('login.html', result=user)

    return response


@app.route('/records/create', methods=['POST'])
def createRecord():
    data = request.json
    payload = jwtService.decode(session['token'])
    print('payload...', payload)
    record = recordService.create({
        **data,
        'user': session['_id']
    })
    return jsonify(record)

@app.route('/records/update', methods=['PUT'])
def updateRecord():
    data = request.json
    print(data)
    record = recordService.update(data.id, data.body)
    return jsonify(record)

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc', host='0.0.0.0', port=5000)
