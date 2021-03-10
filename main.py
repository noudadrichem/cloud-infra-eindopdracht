from flask import Flask, render_template, request, make_response
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
import authomatic
import logging

from config import CONFIG

# Instantiate Authomatic.
authomatic = Authomatic(CONFIG, 'your secret string', report_errors=False)

app = Flask(__name__, template_folder='.')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    # We need response object for the WerkzeugAdapter.
    response = make_response()
    # Log the user in, pass it the adapter and the provider name.
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)

    # If there is no LoginResult object, the login procedure is still pending.
    if result:
        if result.user:
            # We need to update the user to get more info.
            result.user.update()

        # The rest happens inside the template.
        return render_template('login.html', result=result)

    # Don't forget to return the response.
    return response

# Run the app on port 5000 on all interfaces, accepting only HTTPS connections
if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc', host='0.0.0.0', port=5000)
