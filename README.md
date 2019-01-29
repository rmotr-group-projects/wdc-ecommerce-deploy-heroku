<img align="right" width="120" alt="rmotr.com" src="https://user-images.githubusercontent.com/7065401/45454218-80bee800-b6b9-11e8-97bb-bb5e7675f440.png">

# Ecommerce API - Deploy to Heroku

### Setup Instruction

The structure of the whole Django project is built for you. Run the following commands in order to have your local environment up and running.  

```bash
$ mkvirtualenv -p $(which python3) ecommerce
$ pip install -r requirements.txt
```

You can now run the development server and point the browser to the correct URL:

```bash
$ make runserver
```

### Description

The goal of this practice is to perform a deploy of the Ecommerce API project that we've been working on, into a production environment.

For this task you'll need to use the service [Heroku](https://www.heroku.com/), in a similar way that we did during the class.


### Your tasks

Your tasks will be basically focused on following the steps that the instructor showed you during the class.

This would include installing the Heroku CLI, creating the `Procfile` and `runtime.txt` files, configuring some settings and env variables, pushing the project to `heroku` remote repository, etc.

This is a link to a LIVE version of the Ecommerce API, up and running in Heroku:

https://ecommerce-deploy-heroku.herokuapp.com/api/

You can sign in with the following credentials:

```
user: admin
password: admin
```

Also if you get stuck with some of the steps, you can check the `solution` branch in this repository, or take a look at [this project](https://github.com/rmotr-curriculum/wdc-class-7-django-heroku) which is the one showed during the class.
