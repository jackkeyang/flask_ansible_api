# from . import api
from flask import request, current_app, abort, jsonify
from flask.views import MethodView
from app.utils.errors import bad_request, forbidden, unauthorized
from app.utils.ansible_api import Ansible_api
from app import redis_store
from . import mod
# mod = Blueprint('api', __name__)

@mod.before_request
def check_token():
    client_ip = request.remote_addr

    deny_num = redis_store.get(client_ip)
    deny_num = int(deny_num) if deny_num else 0
    if deny_num >= 5:
        return unauthorized()

    TOKEN = current_app.config.get('TOKEN')
    try:
        key = request.headers.get('token')
    except:
        return bad_request()

    if not key or TOKEN != key:
        redis_store.incr(client_ip)
        redis_store.expire(client_ip, 60*5)
        return forbidden()


class AnsibleView(MethodView):
    def get(self):
        tag = request.get_json().get('tag')
        hosts = request.get_json().get('hosts')
        ansible_api = Ansible_api(inventory=hosts,remote_user="root")
        if tag == "module":
            module = request.get_json().get('module')
            args = request.get_json().get('args', None)
            ansible_api.run(module=module, args=args, hosts="all")
        elif tag == "playbook":
            ymls = request.get_json().get('ymls')
            ansible_api.playbook(ymls)
        return jsonify(ansible_api.get_result())

mod.add_url_rule('ansible', view_func=AnsibleView.as_view('ansibleview'))

