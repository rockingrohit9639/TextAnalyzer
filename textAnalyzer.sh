#!/bin/bash

# Installing postgresql as well as other important tools
# These are required by psycopg2 python library
# which in turn are required by django_heroku python library
sudo apt-get -y install postgresql
sudo apt-get -y install libpq-dev python3-dev