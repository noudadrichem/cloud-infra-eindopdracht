from flask import Flask, request, make_response, url_for, redirect, flash, render_template, session
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
import authomatic
import logging

from config import CONFIG

# Instantiate Authomatic.
authomatic = Authomatic(CONFIG, 'AnderG3h3impi3Hi3rzo!', report_errors=False)

app = Flask(__name__, template_folder='html')
app.config['SECRET_KEY'] = 'Sup3rgeheimhee!'

@app.route('/')
def index():
    print('-__session start')
    print(session)
    print('-__session end')
    return render_template('index.html')

@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    # We need response object for the WerkzeugAdapter.
    response = make_response()
    # Log the user in, pass it the adapter and the provider name.
    result = authomatic.login(
        WerkzeugAdapter(request, response),
        provider_name,
        session=session,
        session_saver=lambda: app.save_session(session, response)
    )

    print(session)

    if result:
        if result.user:
            result.user.update()
            session['email'] = result.user.email
            session['id'] = result.user.id
            session['name'] = result.user.name
            session['token'] = 'super geheime token hierzo jeetje zeg'

        return render_template('login.html', result=result)

    return response

# Run the app on port 5000 on all interfaces, accepting only HTTPS connections
if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc', host='0.0.0.0', port=5000)