# Happiness Stars

Keep track of how you are doing in important areas of your life so that you can appreciate what's good and attend to what needs support.


# Project Status

This is a prototype;  with testing, feedback, and a bit of work, I hope I can develop it into a commercial-grade web application while maintaining a [free](https://www.gnu.org/philosophy/free-sw.en.html) codebase.

# Developer Details

## Installation

This is a Django app.

1. Configure a Django project and virtual environment.  I prefer [vex](https://pypi.python.org/pypi/vex).
2. Install via **one** of the following:

  a. `$ pip install git+https://github.com/ptvirgo/hapiness_star_django.git`
  b. `$ git clone https://github.com/ptvirgo/hapiness_star_django.git; cd hapiness_star_django; pip install ./`

3. In your Django settings, set `TEMPLATES[{ .. APP_DIRS: True }]` and add `happiness_star` to INSTALLED_APPS.
