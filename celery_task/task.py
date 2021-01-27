from app import celery
from utils.ansible_api import Ansible_api

@celery.task
def ansibleHocTask(inventory, remote_user, module, args):
    # print(inventory, remote_user, module, args)
    ansible_api = Ansible_api(inventory=inventory, remote_user=remote_user)
    print(ansible_api)
    ansible_api.run(module=module, args=args)
    # print(ansible_api.get_result())
    return ansible_api.get_result()