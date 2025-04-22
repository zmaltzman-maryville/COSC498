TrackPack
======

This is my project for my capstone at Maryville University.
It is built with Flask and using the Flask `tutorial`_ as a starting point.
Images were created using You.com generative AI.

.. _tutorial: https://flask.palletsprojects.com/tutorial/


Install
-------

This application is built on Python version 3.13.2 and recommends using the same version.
Python must be in your PATH, launched from a virtual environment, or specified manually from the bootstrap script.

To prepare the application to run, start by installing from the provided toml file.
From the main directory, execute "pip install ."
This will install dependencies and register TrackPack as an application.

The SQLite3 database will need to be initialized. 
Run "flask --app trackpack -init-db"

Finally, create a copy of the bootstrap script for your environment and edit as necessary. 


Run
---

Assuming all installation steps were completed, simple run your bootstrap script.


Test
----

Unit tests are accomplished using the pytest package. 
To run unit tests, first "pip install pytest" to get the package. 
Then, with your environment active, run "pytest" with any flags you require.
