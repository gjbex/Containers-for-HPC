'''Recipe to create either a docker container or Singularity image
for a compute node on which users can log in using password authentication.
The SQS queue system is available as well as a number of editors, git,
make, CMake, GCC and Open-MPI

Usage:
    $ hpccm  --recipe compute_node.py  --format docker
    $ hpccm  --recipe compute_node.py  --format singularity
'''
# Choose a base image
Stage0.baseimage('ubuntu:20.04')
 
Stage0 += shell(commands=['apt-get update'])

Stage0 += apt_get(ospackages=['python3', ])

Stage0 += apt_get(ospackages=['curl', 'gnupg', 'wget', 'ca-certificates'])

# Stage0 += shell(commands=['curl --insecure https://packages.microsoft.com/keys/microsoft.asc | tac | apt-key add'])
Stage0 += shell(commands=['wget --no-check-certificate -qO -  https://packages.microsoft.com/keys/microsoft.asc > microsoft.asc'])
Stage0 += shell(commands=['apt-key add microsoft.asc'])

Stage0 += shell(commands=['curl --insecure https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list'])
Stage0 += shell(commands=['apt-get update'])
Stage0 += shell(commands=['ACCEPT_EULA=Y apt-get install -y msodbcsql17'])
Stage0 += shell(commands=['ACCEPT_EULA=Y apt-get install -y mssql-tools'])

Stage0 += apt_get(ospackages=['unixodbc',  'unixodbc-dev',  'libodbc1',
                              'odbcinst1debian2', 'tdsodbc'])
Stage0 += apt_get(ospackages=['freetds-bin', 'freetds-common', 'freetds-dev', ])
Stage0 += copy(src=['environment.yml'],
               dest='/var/tmp')
Stage0 += conda(environment='environment.yml', eula=True)
