from app import celery
from utils.ansible_api import Ansible_api

@celery.task
def ansibleHocTask(inventory, remote_user, module, args):
    ansible_api = Ansible_api(inventory=inventory, remote_user=remote_user)
    ansible_api.run(module=module, args=args)
    return ansible_api.get_result()