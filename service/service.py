from flask import Flask, jsonify, send_file, request, render_template
from receive import Archive
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
template_path = os.path.join(os.path.dirname(dir_path), 'client/build')

app = Flask(__name__, template_folder=template_path)

import configparser
config = configparser.ConfigParser()
config.read('etc/conf.ini')


@app.route("/")
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
