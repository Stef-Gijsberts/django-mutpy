django-mutpy
============

Django integration for the mutation testing framework `MutPy`_.

MutPy is a mutation test framework for Python. It basically seeds a bug
into your code and then runs your unit tests to see if they find it.
Mutation testing helps to identify flaws in your tests. Because if your
tests can not uncover obvious bugs, they will also not uncover complex
ones.

This Django app eases the integration of MutPy into your Django project.
It takes care of setting up the Django environment for the tests and
finding the unit tests and the production code.

Requirements
------------

-  Python >= 3.4
-  MutPy >= 0.5.1

Installation
------------

First install the module.

Either

::

    pip install django-mutpy

or download the repository and

::

    git clone https://github.com/phihos/django-mutpy.git
    cd django-mutpy
    python setup.py install

Then add django\_mutpy to the list of installed apps.

.. code:: python

    INSTALLED_APPS = [
      ...
      'django_mutpy',
      ...
      ]

Usage
-----

Run

::

    python manage.py muttest <app1> <app2> ...

.. _MutPy: https://github.com/mutpy/mutpy
