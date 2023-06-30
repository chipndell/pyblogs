# To Initializing this app

clone the app to your convenient path with command for you bash shell:

```
git clone https://github.com/mananbh9/socialpost.git
```

then to install the virtual env specific to the app run the folllowing command in terminal:

```
python3 -m venv venv
```

start the virtual env with command,

```
source venv/bin/activate
cd socialpost/
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



