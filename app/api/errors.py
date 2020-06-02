from flask import jsonify
from . import api

@api.errorhandler(400)
def bad_request():
    respone = jsonify({'error': 'bad request', 'message': "bad request"})
    respone.status_code = 400
    return respone

@api.errorhandler(401)
def unauthorized():
    response = jsonify({'error': 'unauthorized', 'message': 'Not unauthorized'})
    response.status_code = 401
    return response 

@api.errorhandler(403)
def forbidden():
    response = jsonify({'error': 'forbidden', 'message': '403 Forbidden'})
    response.status_code = 403
    return response 

@api.errorhandler(404)
def notfound():
    response = jsonify({'error': 'Not Found', 'message': '404 Not Found'})
    response.status_code = 404
    return response