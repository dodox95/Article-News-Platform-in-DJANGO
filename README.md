Article / News Platform in DJANGO

This platform allows you to create, manage, and publish articles and news stories with ease. Built with Django, it comes with a comprehensive backend interface and support for numerous functionalities, ensuring your content management process is smooth and efficient.
Setup & Installation

Follow these steps to get the platform up and running:
1. Clone the Repository:

bash

git clone https://github.com/travilabs/Article-News-Platform-in-DJANGO.git
cd Article-News-Platform-in-DJANGO

2. Install Dependencies:

Ensure you have Python and pip installed. Then, run:

bash

pip install -r requirements.txt

3. Set the SECRET_KEY:

Open settings.py and set your own SECRET_KEY value. For security reasons, avoid using the default value or publishing your key.
4. Initialize the Database:

bash

python manage.py makemigrations
python manage.py migrate

5. Create a Superuser:

To manage articles, news, and other content, you'll need admin privileges. Create a superuser to access the admin panel:

bash

python manage.py createsuperuser

Follow the prompts to set a username, email, and password for the superuser.
6. Run the Django Application:

bash

python manage.py runserver

Visit http://127.0.0.1:8000/admin/ in your browser and log in with the superuser credentials to access the admin panel. From here, you can manage, add, or delete articles and news.
Usage:

    After starting the application, head to the admin panel (/admin/) to manage your content.
    Add, edit, or delete articles and news as per your requirements.
    To see the content on the front-end, navigate to the platform's main page.

Contribution:

Feel free to fork this repository and contribute. Pull requests, bug fixes, and new features are always welcome!

Remember to make necessary modifications based on your exact project specifications and directory structure. This README provides a general outline for setting up and running a Django project.
