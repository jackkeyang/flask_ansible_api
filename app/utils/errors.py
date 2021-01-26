from flask import jsonify
# from . import mod
from app.views import mod 

@mod.errorhandler(400)
def bad_request():
    respone = jsonify({'error': 'bad request', 'message': "bad request"})
    respone.status_code = 400
    return respone

@mod.errorhandler(401)
def unauthorized():
    response = jsonify({'error': 'unauthorized', 'message': 'Not unauthorized'})
    response.status_code = 401
    return response 

@mod.errorhandler(403)
def forbidden():
    response = jsonify({'error': 'forbidden', 'message': '403 Forbidden'})
    response.status_code = 403
    return response 

@mod.errorhandler(404)
def notfound():
    response = jsonify({'error': 'Not Found', 'message': '404 Not Found'})
    response.status_code = 404
    return response