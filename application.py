from flask import Flask

# Elastic Beanstalk looks for 'application' by default
application = Flask(__name__)

@application.route('/')
def home():
    return "Hello from Python on AWS Elastic Beanstalk!"

@application.route('/health')
def health_check():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)