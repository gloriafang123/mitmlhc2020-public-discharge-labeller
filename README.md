# django_learning_2

1. Install Django (pip install django), using python 3.
2. Pickle your own word embeddings (a dictionary mapping word to vector) in the folder highlighter/load. This file is usually large and cannot be pushed to git.
3. run: python manage.py runserver
4. use adminDB link to navigate the labelled summaries you've saved.
CAUTION: if pushing to a public git repo, be sure to DELETE your database (or .gitignore it), otherwise the discharge summaries will be publicly visible. (Name of the current database is db.sqlite3).
Also, may want to add your own superuser with username and password for admin db management.
