# Peatus backend
# Django Framework

Requirements:
```
Python >3.10
```

**DO NOT FORGER CREATE AND ADD TO .env FILE FOLLOWING ENVIRONMENT VARIABLES**

```shell
SECRET_KEY=12343534tdsjbfsdigfuhsdiugbsdg
DATABASE_URL=psql://username:password@127.0.0.1:5432/databasename
```

1. Step: Create Virtual Environment

```shell
python -m venv venv
```

Activate Virtual Environment

On Linux: `source venv/bin/activate`

On Windows: `venv/Scripts/activate`

2. Step: Install requirements

```shell
pip install -r requirements.txt 
```

3. Step: Run gunicorn server

```shell
gunicorn runserver 0.0.0.0:8000
```
