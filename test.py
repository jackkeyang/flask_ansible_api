import requests

#data = {
#        "tag": "module",
#        "hosts": "192.168.0.100, 192.168.0.108",
#        "module": "ping",
#        "args": "",
#        "token": "jopUIHp1239Oads"
#        }

data = {
        "tag": "playbook",
        "hosts": "192.168.0.100, 192.168.0.108",
        "ymls": ["/home/flask_ansible_api/playbooks/test.yml"],
        "token": "jopUIHp1239Oads"
        }

resp = requests.get('http://localhost:5000/api/ansible', json=data)
print resp.content
