from flask import Flask, request, make_response, url_for, redirect, flash, render_template, session, jsonify
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
import authomatic
import logging
import datetime
import uuid
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

def getUserFromSes():
    token = request.headers.get('Token')
    print('tok 1 ', token)
    if token == None:
        print('tok 2', token, session)
        if session.get('token'):
            token = session.get('token')
            print('tok 3', token)
        else:
            print('GO HOME')
            redirect('/')
    print('tok 4 ', token)
    user = userService.getByToken(token)
    print('user 4', user)
    if user == None:
        print('user none.. GO HOME',)
        redirect('/')

    print('USER 5...', user)
    return user

@app.route('/')
def index():
    user = getUserFromSes()
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

    if result:
        print('result', result)
        if result.user:
            result.user.update()
            user = userService.getByGoogleId(result.user.id)
            print('User', user)
            token = uuid.uuid4().hex
            if user == None:
                user = userService.create({
                    'email': result.user.email,
                    'name': result.user.name,
                    'googleId': result.user.id,
                    'token': token
                })
            else:
                user = userService.update(user['_id'], { 'token': token })
            session['token'] = token
            session['user'] = user['_id']
            return redirect('/dashboard')

        return render_template('login.html', result=user)

    return response

# UI
@app.route('/dashboard', methods=['GET'])
def dashboard():
    user = getUserFromSes()
    return render_template('dashboard.html', user=user)

@app.route('/dashboard/create', methods=['GET'])
def dashboardCreate():
    user = getUserFromSes()
    return render_template('create-record.html', user=user)

@app.route('/dashboard/update/<record_id>', methods=['GET'])
def dashboardUpdate(record_id):
    print('Record id...', record_id)
    user = getUserFromSes()
    record = recordService.getById(record_id)
    print('record.', record)
    return render_template('update-record.html', user=user, record=record)

@app.route('/dashboard/delete/<record_id>', methods=['GET'])
def dashboardDelete(record_id):
    print('Record id...', record_id)
    user = getUserFromSes()
    record = recordService.getById(record_id)
    print('record.', record)
    return render_template('delete-record.html', user=user, record=record)

# RECORDS REST
@app.route('/records', methods=['GET'])
def getUserRecords():
    user = getUserFromSes()
    records = recordService.getByUserId(str(user['_id']))
    print('records...', records)
    return jsonify(records)

@app.route('/records/create', methods=['POST'])
def createRecord():
    user = getUserFromSes()
    body = request.json
    print('body ...', body)
    record = recordService.create({
        'domain': body['domain'],
        'ipv4': body['ipv4'],
        'ipv6': body['ipv6'],
        'user': body['user'],
        'createdAt': datetime.datetime.now()
    })
    print('created record...', record)

    return jsonify(record)

@app.route('/records/update', methods=['PUT'])
def updateRecord():
    user = getUserFromSes()
    if user == None:
        redirect('/')
    body = request.json
    print(body)
    record = recordService.update(body)
    return jsonify(record)

@app.route('/records/delete', methods=['DELETE'])
def deleteRecord():
    body = request.json
    user = getUserFromSes()
    if user == None:
        redirect('/')
    print('Delete record...', body)
    recordService.delete(body['id'])
    return jsonify({
        'message': 'deleted...'
    })

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc', host='0.0.0.0', port=5000)
