from flask import (
    request,
    Blueprint,
    abort,
    jsonify,
    g,
)


main = Blueprint('api', __name__)


@main.route('/update', methods=['GET'])
def api_update():
    return jsonify({
        'name': 'Overwatch Replay Analyzer',
        'version': 0.1,
        'status': 'Beta',
        'release_date': '2018-02-12',
        'changelog': 'changelog test',
        'alert': 'alert test',
        'notice': 'notice test',
        'donation': 0,
        'donation_current': 0.0,
    })
