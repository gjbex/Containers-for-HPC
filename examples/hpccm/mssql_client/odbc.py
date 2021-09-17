'''Recipe to create either a docker container or Singularity image
for an MS SQL SErver client.

Usage:
    $ hpccm  --recipe odbc.py  --format docker
    $ hpccm  --recipe odbc.py  --format singularity
'''
# Choose a base image
Stage0.baseimage('ubuntu:20.04')
 
# Update package repositories 
Stage0 += shell(commands=['apt-get update'])

# install software for getting and installing the Microsoft drivers
Stage0 += apt_get(ospackages=['curl', 'gnupg', 'ca-certificates'])

# get Microsoft repository certificate
Stage0 += shell(commands=['curl --insecure https://packages.microsoft.com/keys/microsoft.asc > microsoft.asc',
                          'apt-key add microsoft.asc'])

# get Microsoft package list
Stage0 += shell(commands=['curl --insecure https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list'])

# refresh package list to take Microsoft software into account
Stage0 += shell(commands=['apt-get update'])

# install the drivers
Stage0 += shell(commands=['ACCEPT_EULA=Y apt-get install -y msodbcsql17'])
Stage0 += shell(commands=['ACCEPT_EULA=Y apt-get install -y mssql-tools'])

# install ODBC and FreeTDS libraries
Stage0 += apt_get(ospackages=['unixodbc',  'unixodbc-dev',  'libodbc1',
                              'odbcinst1debian2', 'tdsodbc'])
Stage0 += apt_get(ospackages=['freetds-bin', 'freetds-common', 'freetds-dev', ])

# copy the conda environment into the container
# Stage0 += copy(src=['environment.yml'],
#                dest='/var/tmp')

# install the environment
Stage0 += conda(packages=['pyodbc', 'pymssql', 'xlrd=1.2.0'], eula=True)
