# Gunicorn configuration file

bind = '0.0.0.0:8000'

loglevel = 'info'
errorlog = '-'
accesslog = '-'
workers = 1
limit_request_line = 16384
limit_request_fields = 200
