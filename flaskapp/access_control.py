from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from functools import wraps
from flask import jsonify

# Custom decorator for filter routes for operator
def operator_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] != 'operator':
            return {"error":"Only for operators!"}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper