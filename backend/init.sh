#!/bin/bash

apps=(systems tools notices stocks)
rm -rf core.db
for app in ${apps[@]};do
  rm -rf $app/migrations
done

for app in ${apps[@]};do
  echo $app
  python manage.py makemigrations $app
done

python manage.py migrate
python manage.py init_sys
python manage.py runserver