from flask import Flask, jsonify, send_file, request, render_template
from flask_security import MongoEngineUserDatastore, Security, \
        auth_token_required, anonymous_user_required
from flask_security.utils import hash_password

from api.app import app, db
from api.receive import Archive
from api.model.user import User
from api.model.role import Role

# Read server config file
import configparser
config = configparser.ConfigParser()
config.read('etc/conf.ini')

# Flask config
app.config['SECRET_KEY'] = 'security key!!!!'

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
app.config['SECURITY_PASSWORD_SALT'] = '!!!super secret salt!!!'
app.config['SECURITY_TOKEN_AUTHENTICATION_KEY'] = True

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.route("/api/login")
def login():
    return 'some shit'

@app.route("/")
@auth_token_required
def root():
    return render_template("index.html")


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
    # Archive.validate中会隐式的判断文件名是否符合标准
    file.save(os.path.join('files', 'data', file.filename))
    return 'ok', 204

if __name__ == "__main__":
    app.run(host='0.0.0.0')
