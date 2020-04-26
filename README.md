# Hotel Bot

This is small telegram bot that was developed as test task to an internship. 

It was written on Python 3.7 using django framework.



## Running the bot

* To run this bot you need to install Python 3.7 on your machine and pipenv.

  `sudo apt install python3.7`

  `pip install pipenv` 

* After that you need to install from pipfile:

  `pipenv install`

* And activate pipenv shell:

  `pipenv shell`

* After everything is done, you can run the bot. Use the following command to do it:

  `python manage.py run_bot`

* If you want to go to the admin panel you need to run the application:

  `	python manage.py runserver`

The database is already created so you can go to localhost:8000/admin and use "**artem**" as username and "**test1234**" as password.