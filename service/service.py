from flask import Flask, jsonify, send_file, request, \
render_template, send_from_directory, session
from flask_security import MongoEngineUserDatastore, Security, \
        login_required
from flask_security.utils import hash_password
from flask_mail import Mail
from flask_wtf import FlaskForm

from api.app import app, db, statc_path, template_path
from api.receive import Archive
from api.model.user import User
from api.model.role import Role

# Read server config file
import configparser
config = configparser.ConfigParser()
config.read('etc/conf.ini')

# Flask config
app.config['SECRET_KEY'] = '!!!security key!!! change in production'

# MongoDB config
app.config['MONGODB_DB'] = 'ora'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017

# Security config
app.config['SECURITY_TRACKABLE'] = True
app.config['SECURITY_CONFIRMABLE'] = True
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
app.config['SECURITY_PASSWORD_SALT'] = '!!!super secret salt!!! change in production'
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = True
app.config['SECURITY_EMAIL_SENDER'] = 'ora@owdata.org'
app.config['SECURITY_URL_PREFIX'] = '/api'

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Mail setup
app.config['MAIL_DEFAULT_SENDER'] = 'ora@owdata.org'
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'user'
app.config['MAIL_PASSWORD'] = 'password'
mail = Mail(app)

@app.route("/")
def root():
    form = FlaskForm()
    return render_template("index.html", form=form)

# Reserve url for redux router
@app.route("/route/<path:path>")
def redux_route(path):
    form = FlaskForm()
    return render_template("index.html", form=form)

@app.route("/api/check_update/<os>/<current>")
def check_update(os, current):
    latest_version = config['update']['client_version']
    if current < latest_version:
        return jsonify({'is_latest':False,
                        'url': '{}download/client/{}/{}'.format(config['host']['url'], os, latest_version)})
    else:
        return jsonify({'is_latest':True})


@app.route("/download/client/<os>/<path>")
def client_download(os, path):
    if path is None:
        return 'invalid argument', 400
    try:
        return send_file('files/{}/ora-{}.zip'.format(os, path), as_attachment=True)
    except Exception as err:
        return 'file not found', 404


@app.route('/receive', methods=['POST'])
def receive():
    file = request.files['ora_file']
    suffix = file.filename.split('.')[-1]
    if suffix not in ['zip', 'rar']:
        return 'file format error', 403
    if not Archive.validate(file, suffix):
        return 'json error', 403

    path = os.path.join('files', 'data')
    if not os.path.exists(path):
        os.makedirs(path)

    file.save(Archive.rename(file.filename, path))
    return 'ok', 204

# Dev static server DO NOT USE IN PRODUCTION
# @app.route('/static/js/<path:path>')
# def send_js(path):
#     return send_from_directory(statc_path + '/js', path)

# @app.route('/static/css/<path:path>')
# def send_css(path):
#     return send_from_directory(statc_path + '/css', path)

# @app.route('/static/media/<path:path>')
# def send_media(path):
#     return send_from_directory(statc_path + '/media', path)

# @app.route('/service-worker.js')
# def send_sw_js():
#     return send_from_directory(template_path , 'service-worker.js')

# @app.route('/manifest.json')
# def send_manifest():
#     return send_from_directory(template_path , 'manifest.json')

# @app.route('/asset-manifest.json')
# def send_asset_manifest():
#     return send_from_directory(template_path , 'asset-manifest.json')

# @app.route('/favicon.ico')
# def send_favicon():
#     return send_from_directory(template_path , 'favicon.ico')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
