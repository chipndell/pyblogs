# To Initializing app

``` python
git clone git@github.com:chipndell/pyblogs.git
cd pyblogs/
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

To initialize the database run the commnad:

``` python
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

Environment Variables for app

- SECRET
- DEBUG
- HOST _A Database Host address like `user.database.example.com`_
- MY_SQL_PASSWORD
- MY_SQL_USER
- MY_SQL_DATABASE
- PYBLOG_API_TOKEN
