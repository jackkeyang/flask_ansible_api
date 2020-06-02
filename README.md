# flask_ansible_api

# run
```
gunicorn app:create_app\(\'dev\'\) -w 10 -b 0.0.0.0:5000
```

# run module
```
import requests

data = {
        "tag": "module",
        "hosts": "192.168.0.100, 192.168.0.101",
        "module": "ping",
        "args": "",
        "token": "jopUIHp1239Oads"
        }

resp = requests.get('http://localhost:5000/api/ansible', json=data)
print resp.content
```

# run playbook
```
import requests

data = {
        "tag": "playbook",
        "hosts": "192.168.0.100, 192.168.0.101",
        "ymls": ["playbooks/test.yml"],
        "token": "jopUIHp1239Oads"
        }
        
resp = requests.get('http://localhost:5000/api/ansible', json=data)
print resp.content
```
