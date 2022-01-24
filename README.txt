The included source has been written in Django 3.0. All source code has been tested and will run unmodified on Django 2.2, except for the MariaDB configuration files as MariaDB support was not added until Django 3.0.

The source has been tested against the version of SQLite that comes with Django. While the data structures used in the book are simple and shouldn't cause problems if you decide to use another database, there are no guarantees. If you find any database-related quirks, refer to the database engine documentation.

The source is broken up into folders, one for each chapter of the book. Rather than delete code that changes from chapter to chapter, I have commented out lines of code in the source so you can see where the code has changed.

Code line numbering in the book is provided so you can easily cross-reference my explanations to individual lines of code in the book. In most cases, line numbering in the book does not match line numbers in the source files.

The source is not designed to be executed as is. The SQLite database file and migrations for each chapter has been removed from the source. While copying the source code from a chapter and running it inside a virtual environment will work in most cases (after running the migrations), there is no guarantee it will. The source code is for your reference and to assist your learning, it's not fully functioning code that you can just copy and use in your projects.

## Reporting Bugs

You can contact me via the [help page](https://djangobook.com/django-help/) on the Djangobook website to report any bugs in the code.