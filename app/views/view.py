# from . import api
from flask import request, current_app, abort, jsonify
from flask.views import MethodView
from utils.errors import bad_request, forbidden, unauthorized
from utils.ansible_api import Ansible_api
from app import redis_store, celery
from celery_task.task import ansibleHocTask
from . import mod
# mod = Blueprint('api', __name__)

@mod.before_request
def check_token():
    '''
    验证token， 如果同一IP认证失败5次，则封禁5分钟
    '''
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
        module = request.get_json().get('module')
        args = request.get_json().get('args', None)
        if tag == "module":
            result = ansibleHocTask.delay(hosts, "root", module, args)
        elif tag == "playbook":
            ymls = request.get_json().get('ymls')
            ansible_api.playbook(ymls)
        return jsonify({'code': 200, 'result_id': result.id})

class AnsibleResultView(MethodView):
    def get(self, result_id):
        result = celery.AsyncResult(id=result_id)
        return jsonify({'code': 200, 'result': str(result.get())})

mod.add_url_rule('/ansible', view_func=AnsibleView.as_view('ansibleview'))
mod.add_url_rule('/ansible/<string:result_id>', view_func=AnsibleResultView.as_view('ansibleresultview'))

