from app import create_app
from flask_script import Manager

app = create_app('dev')
manager = Manager(app)

def main():
    manager.run()

if __name__ == '__main__':
    manager.run()
