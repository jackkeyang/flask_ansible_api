from . import api
from utils import config
from flask import request, current_app, abort
from errors import *
from ansible_api import Ansible_api


@api.before_request
def check_token():
    TOKEN = current_app.config.get('TOKEN')
    try:
        key = request.get_json().get('token')
    except:
        return bad_request()
    if not key or TOKEN != key:
        return forbidden()

@api.route('/ansible')
def ansible():
    # 
    # module: {"tag": "module", "hosts": "192.168.1.2,...", "module": "shell", "args": "xxx"}
    # playbook: {"tag": "playbook", "hosts": "192.168.1.2,..." ,"ymls": ["/etc/ansible/site1.yml", "....."]}
    #
    tag = request.get_json().get('tag')
    hosts = request.get_json().get('hosts')
    ansible_api = Ansible_api(hosts)

    if tag == "module":
        module = request.get_json().get('module')
        args = request.get_json().get('args', None)
        ansible_api.run(module, args, "all")
    elif tag == "playbook":
        ymls = request.get_json().get('ymls')
        ansible_api.playbook(ymls)
    return jsonify(ansible_api.get_result())
