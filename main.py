from flask import Flask, request, make_response, url_for, redirect, flash, render_template, session, jsonify
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
import authomatic
import logging
import datetime
import uuid
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from services.databaseService import DatabaseService
from services.userService import UserService
from services.recordService import RecordService
from services.dnsService import DNSService
from config import CONFIG

# Instantiate Authomatic.
authomatic = Authomatic(CONFIG, 'AnderG3h3impi3Hi3rzo!', report_errors=False)

sentry_sdk.init(
    dsn="https://e873b73e2f9b4016856461703a2fe233@o561444.ingest.sentry.io/5698868",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

app = Flask(__name__, template_folder='html')
app.config['SECRET_KEY'] = 'Sup3rgeheimhee!'

db = DatabaseService()
userService = UserService(db)
recordService = RecordService(db)
dnsService = DNSService()

def getUserFromSes():
    token = request.headers.get('Token')
    if token == None:
        if session.get('token'):
            token = session.get('token')
        else:
            redirect('/')
    user = userService.getByToken(token)
    if user == None:
        redirect('/')
    print('user...', user)
    return user

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({
        'message': 'logged out'
    })

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

# ? UI
@app.route('/dashboard', methods=['GET'])
def dashboard():
    print('session...', session)
    user = getUserFromSes()
    return render_template('dashboard.html', user=user)

@app.route('/dashboard/create', methods=['GET'])
def dashboardCreate():
    user = getUserFromSes()
    return render_template('create-record.html', user=user)

@app.route('/dashboard/update/<record_id>', methods=['GET'])
def dashboardUpdate(record_id):
    user = getUserFromSes()
    record = recordService.getById(record_id)
    return render_template('update-record.html', user=user, record=record)

@app.route('/dashboard/delete/<record_id>', methods=['GET'])
def dashboardDelete(record_id):
    print('Record id...', record_id)
    user = getUserFromSes()
    record = recordService.getById(record_id)
    print('record.', record)
    return render_template('delete-record.html', user=user, record=record)

# ? REST
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

    print('ADD ARGS...', record['domain'], record['ipv4'])
    dnsService.add(record['domain'], record['ipv4'])

    print('created record...', record)

    return jsonify(record)

@app.route('/records/update', methods=['PUT'])
def updateRecord():
    user = getUserFromSes()
    if user == None:
        redirect('/')
    body = request.json
    print(body)
    print('UPDATE ARGS...', body['domain'], body['ipv4'])
    dnsService.update(body['domain'], body['ipv4'])
    record = recordService.update(body)
    return jsonify(record)

@app.route('/records/delete', methods=['DELETE'])
def deleteRecord():
    body = request.json
    user = getUserFromSes()
    record = recordService.getById(body['id'])
    if user == None:
        redirect('/')
    print('delete record...', record)
    dnsService.delete(record['domain'])
    recordService.delete(record['_id'])
    return jsonify({
        'message': 'deleted...'
    })

@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000,
        host='0.0.0.0'
        # ssl_context='adhoc',
    )
