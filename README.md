# Society of Freedom REST API

The Society of Freedom implements all neccessary features and tools for web
networking among people. It allows authorized usersto create, edit, delete posts. If you like post of other users you can mark it as a 'liked' post.
Security of your data is guarded enough. It achived with JWT Autorization,
which is a new standard of network security.
Third party API [Emailhunter](https://hunter.io) verify users email for
validity.

## Getting Started
Please follow the instructions bellow in order to successfully run the API.

## Prerequisites

You should have at least Python version 3.6 and PostgresSQL database installed on your local machine to be able to use this application. 
Preferably to run this app in isolated virtual environment, thus you should
create venv in the beginning:
```
python3 -m venv <name_of_your_venv> # or any other tools

```
All dependencies are listed in **requirements.txt** To install the latter simply enter in either terminal or a prompt the following command:

```
pip install -r requirements.txt

```

## Installing

Clone this repo onto your local machine by the following command:

### https
```
git clone https://github.com/AleksMD/social_network.git

```
N.B. Database in postgres should be created before you start running the application.
To do so, open postgres db in terminal by this command:

```
sudo -u postgres psql

```
In opened terminal window enter:

```
CREATE DATABASE name_of_your_app_database;

```

Create user in postgres:

```
CREATE USER your_user_name WITH PASSWORD 'your_password';

```

Grant access to the database to the user:
```
GRANT ALL PRIVILEGES ON DATABASE name_of_your_app_database TO your_user_name;
```

After database was created update DATABASE section in settings.py
### Info
***In order to be able to use email hunter service you should have valid
api_key. In app settings it set to None by DEFAULT***
To get EmailHunter API key sign up on their official web site.

## Start API
To start the app activate virtual environment by the following command:

```
source <path_to_virtual_env_folder>/bin/activate

```
and then run following command in terminal in root directory of the project:

```
python manage.py runserver

```
If the start of this app is succussfull you can open an internet browser and go to an index page:

```
http://127.0.0.1:8000/ 

```
If there are no errors it means that everything works fine.

See next section to understand how you run tests.
## API Endpoints
*You can user either desktop(Postman, Insomnia etc.) or console(curl, http
etc.) tools for accessing API*
> Sign Up:
```
curl -d "{\"username\": \"<your_username\">,\"password\":\"<your_password>\"}" -H "Content-Type: application/json"
  http://localhost:8000/signup/
```
> Get access token:
```
curl -d "{\"username\": \"<your_username\">,\"password\":\"<your_password>\"}" -H "Content-Type: application/json"
  http://localhost:8000/api/token/
```
> List of all users:
```
curl -H "Authorization: Bearer <your_token_from_previous_step>"
  http://localhost:8000/users/

```
> Particular user:
```
curl -H "Authorization: Bearer <your_token>"
  http://localhost:8000/users/<user_id>/
```
> List of all posts:
```
curl -H "Authorization: Bearer <your_token>"
  http://localhost:8000/posts/
```
> Particular post:
```
curl -H "Authorization: Bearer <your_token>"
  http://localhost:8000/posts/<post_id>/
```
>> N.B. Even though you are able to get data from database, at the very first
>> time you run the app database is empty. Next version of the app will be
>> provided with predefined data.
> Create post:
```
curl -d "{\"title\": \"<post_title>\">,\"content\":\"<post_content>\"}" -H "Content-Type: application/json" -H "Authorization: Bearer <your_token>"
http://localhost:8000/create_new_post/
```

## Running the tests
There  lots of test cases for this application.
To run all of those use following command:

```
python -m manage test

```
or

```
python manage.py test

```
The difference between both of the above you can find [here.](https://docs.python.org/3/using/cmdline.html)

If you are interested in testing particular test case each test marks by
intuitively undestandable tags. To use that just run the following command:
```

python manage.py test --tag=<tag_name>

```
## Future Development
In nearest future database fixtures will be implemented for improving testing
workflow.
Clearbit service is going to be implemented in v0.0.2. Details about this third
party API [here.](https://clearbit.com/docs)
## Built With

* [Python3.7](https://www.python.org) - The programming language of the app
* [Django framework](https://www.djangoproject.com/) - The web framework used
* [Django REST framework](https://www.django-rest-framework.org/) - The web framework used
* [PostgresSQL](https://rometools.github.io/rome/) - The relational database used

## Versioning

Version 0.0.1

## Authors

* **Oleksandr Budonniy** - *Initial work* - [AleksMD](https://github.com/AleksMD)

## License

Under no license

