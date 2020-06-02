import json
from collections import namedtuple
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible import context
import ansible.constants as C
import os
import shutil

class ResultCallback(CallbackBase):
    def __init__(self):
        super(ResultCallback,self).__init__()
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_ok(self, result, **kwargs):
        self.host_ok[result._host] = result._result

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host] = result._result

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.host_failed[result._host] = result._result

class Ansible_api:
    def __init__(self, hostlist=None):
        self.loader = DataLoader()
        # self.variable_manager = VariableManager()
        self.inventory = InventoryManager(loader=self.loader, sources='%s,'%hostlist)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.results_callback = ResultCallback()
        context.CLIARGS = ImmutableDict(
            connection='ssh', 
            module_path=None, 
            forks=10, 
            become=None, 
            timeout=30,
            become_method=None, 
            become_user=None, 
            check=False, 
            diff=False,
            syntax=None,
            start_at_task=None
        )
    
    def run(self, module, args, ansible_hosts):
        play_source = {
            "name": "ansible api run_adhoc",
            "hosts": ansible_hosts,
            "gather_facts": "no",
            "tasks": [
                {"action": {"module": module, "args": args}}
            ]
        }

        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory = self.inventory,
                variable_manager = self.variable_manager,
                loader = self.loader,
                passwords = None,
                stdout_callback = self.results_callback
            )
       
            result = tqm.run(play)
        finally:
            if tqm is not None: 
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def playbook(self, yaml_file_list):
#        self.variable_manager.extra_vars = {"host": host}
        pb = PlaybookExecutor(
            playbooks=yaml_file_list,
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            passwords = None,
        )
        pb._tqm._stdout_callback = self.results_callback
        result = pb.run()

    def get_result(self):
        result_raw = {'success':{},'failed':{},'unreachable':{}}
      
        for host,result in self.results_callback.host_ok.items():
            result_raw['success']["%s"%host] = result
        for host,result in self.results_callback.host_failed.items():
            result_raw['failed']["%s"%host] = result
        for host,result in self.results_callback.host_unreachable.items():
            result_raw['unreachable']["%s"%host] = result
        
        return json.dumps(result_raw, indent=4)

if __name__ == '__main__':
    ansible_api = Ansible_api('192.168.0.100, 192.168.0.108')
    #ansible_api.run("ping", "","all")
    #ansible_api.get_result()
    ansible_api.playbook(["/devops/bp.yml"])
    print ansible_api.get_result()
