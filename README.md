# To Initializing this app

clone the app to your convenient path with command for you bash shell:

```
git clone https://github.com/chipndell/pyblogs.git
```

then to install the virtual env specific to the app run the folllowing command in terminal:

```
python3 -m venv venv
```

start the virtual env with command,

```
source venv/bin/activate
cd pyblogs/
```

To install all the dependencies related to this app run the follwing command:

```
pip3 install -r requirements.txt
```

To initialize the database run the commnad:

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

There you have it working...


Provide password in the production server with,

os.environ['SECRET'] = ''
os.environ['DEBUG'] = ''
os.environ['MY_SQL_PASSWORD'] = ''
os.environ["HOST"] = ""
os.environ["MY_SQL_USER"] = ""
os.environ["MY_SQL_DATABASE"] = ""
os.environ["PYBLOG_API_TOKEN"] = ""
