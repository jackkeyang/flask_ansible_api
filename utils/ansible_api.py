import json
import shutil
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible import context
import ansible.constants as C


class ResultCallback(CallbackBase):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_ok(self, result, **kwargs):
        self.host_ok[result._host.get_name()] = result._result

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result._result

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.host_failed[result._host.get_name()] = result._result

class Ansible_api():
    def __init__(self,
        connection="ssh", # 连接方式： local 本地， smart ssh
        remote_user=None,
        remote_password=None,
        private_key_file=None,
        sudo=None,  sudo_user=None, ask_sudo_pass=None,
        module_path=None,
        become=None,            # 是否提权  
        become_method=None,     # 提权方式， 默认sudo，可以是su   
        become_user=None,       # 提权后要成为的用户，并非登录用户
        check=False, diff=False,
        listhosts=None, listtasks=None, listtags=None,
        verbosity=3,
        syntax=None,
        start_at_task=None,
        inventory=None):

        context.CLIARGS = ImmutableDict(
            connection = connection,
            remote_user = remote_user,
            private_key_file = private_key_file,
            sudo = sudo,
            sudo_user = sudo_user,
            ask_sudo_pass = ask_sudo_pass,
            module_path = module_path,
            become = become,
            become_method = become_method,
            become_user = become_user,
            verbosity = verbosity,
            listhosts = listhosts,
            listtasks = listtasks,
            listtags = listtags,
            syntax = syntax,
            start_at_task = start_at_task,
        )

        self.inventory = "%s,"%",".join(inventory) if isinstance(inventory, list) else []
        
        # 实例化数据解析器
        self.loader = DataLoader()
        # 实例化 资产配置对象
        self.inv_obj = InventoryManager(loader=self.loader, sources=self.inventory)
        # 设置密码
        self.passwords = remote_password
        # 实例化回调插件对象
        self.results_callback = ResultCallback()
        # 变量管理器
        # self.variable_manager = VariableManager(self.loader, self.inv_obj)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inv_obj)

    def run(self, hosts="all", gether_facts="no", module="ping", args="", task_time=0):
            '''
            task_time:  执行异步任务等待的秒数，这个需要大于0， 等于0的时候不支持异步。 默认值：0
            '''
            play_source = dict(
                name = "Ad-hoc",
                hosts = hosts,
                gather_facts = gether_facts,
                tasks = [
                    {"action": {"module": module, "args": args}, "async": task_time, "poll": 0}
                ]
            )
            play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
            tqm = None
            try:
                tqm = TaskQueueManager(
                    inventory = self.inv_obj,
                    variable_manager = self.variable_manager,
                    loader = self.loader, 
                    passwords = self.passwords,
                    stdout_callback = self.results_callback
                )
                result = tqm.run(play)
            except Exception as e:
                print(e)
            finally:
                if tqm is not None:
                    tqm.cleanup()
                shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def playbook(self, playbooks):
        '''
        playbooks: 是一个列表类型
        '''
        from ansible.executor.playbook_executor import PlaybookExecutor

        playbook = PlaybookExecutor(playbooks=playbooks,
                        inventory=self.inv_obj,
                        variable_manager=self.variable_manager,
                        loader=self.loader,
                        passwords=self.passwords)
                    
        playbook._tqm._stdout_callback = self.results_callback
        result = playbook.run()

    def get_result(self):
        result_raw = {'success':{},'failed':{},'unreachable':{}}
      
        for host,result in self.results_callback.host_ok.items():
            result_raw['success'][host] = result
        for host,result in self.results_callback.host_failed.items():
            result_raw['failed'][host] = result
        for host,result in self.results_callback.host_unreachable.items():
            result_raw['unreachable'][host] = result
        # return json.dumps(result_raw, indent=4)
        # print(json.dumps(result_raw, indent=4))
        return json.dumps(result_raw)

if __name__ == '__main__':
    ansible = Ansible_api(inventory=["192.168.0.109", "localhost", "192.168.0.101"], remote_user="root")
    ansible.run()
    # ansible.playbook(["/Users/jack/Development/flask_ansible_api/playbooks/test.yml"])
    print(ansible.get_result())
