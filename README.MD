# SIMPLE RSA IMPLEMENTATION IN DJANGO

## Technologies Used
- Django
- DaisyUI

## Environment
- Python 3.10.X
- PIP 22.3.X

# How to run on dev mode

- Create a virtual environment for python (you can use virtualenv, venv, poetry, etc)

```console
nefonfo@nefonfo-pc:~$ virtualenv env
nefonfo@nefonfo-pc:~$ source env/bin/activate
(env) nefonfo@nefonfo-pc:~$ 
```

- Install the pip requirements (requirements.txt)
```console
(env) nefonfo@nefonfo-pc:~$ pip install -r requirements.txt
```

- Create the DB
```console
(env) nefonfo@nefonfo-pc:~$ python manage.py migrate
```

- Create the Superuser
```console
(env) nefonfo@nefonfo-pc:~$ python manage.py createsuperuser
```

- Create the RSA private and public key
```console
(env) nefonfo@nefonfo-pc:~$ python manage.py generate_keys
--- KEYS CREATED SUCCESSFULLY ---
```

- Run server
```console
(env) nefonfo@nefonfo-pc:~$ python manage.py runserver
```

And that's all... Go to https://localhost:8000 for the app and https://localhost:8000/admin for admin managements. 