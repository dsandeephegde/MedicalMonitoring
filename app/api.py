from flask import request

from app import AEModels
from app import app


@app.route('/ae/lof', methods=['POST'])
def lof():
    request_json = request.get_json()
    data = AEModels.lof(request_json['table'], request_json['tests'])
    return data.to_json()
