import os

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'local')

if ENVIRONMENT == 'production':
    import pymysql
    pymysql.install_as_MySQLdb()
# else:
#     import subprocess
#     os.chdir("../")
#     bashCommand = "bash scripts/load_sample_data.sh"
#     process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
#     output, error = process.communicate()