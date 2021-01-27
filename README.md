# flask_ansible_api

# run
```
gunicorn app:create_app\(\'dev\'\) -w 10 -b 0.0.0.0:5000
```
或者
```
python run.py runserver -h 0.0.0.0
```

# 运行celery
`celery -A app.celery worker --loglevel=info`
> flask 中使用celery 返回结果为空，需要在运行celery的终端中定一个环境变量：export PYTHONOPTIMIZE=1


# run module
```
import requests

headers = {"token": "jopUIHp1239Oads"}

data = {
        "tag": "module",
        "hosts": "192.168.0.100, 192.168.0.101",
        "module": "ping",
        "args": "",
        }

resp = requests.get('http://localhost:5000/api/ansible', json=data, headers=headers)
print resp.content
```

# run playbook
```
import requests

headers = {"token": "jopUIHp1239Oads"}

data = {
        "tag": "playbook",
        "hosts": "192.168.0.100, 192.168.0.101",
        "ymls": ["playbooks/test.yml"],
        }
        
resp = requests.get('http://localhost:5000/api/ansible', json=data, headers=headers)
print resp.content
```

以上运行返回一个result_id: 7fa58734-2e8b-4b94-8b82-b460ec875dda

# 通过result_id 获取返回信息
```
import requests
import json

headers = {"token": "jopUIHp1239Oads"}

resp = requests.get('http://localhost:5000/api/ansible/7fa58734-2e8b-4b94-8b82-b460ec875dda', headers=headers)
data = json.loads(resp.content)

```
