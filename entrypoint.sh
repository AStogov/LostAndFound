#!/bin/bash

if [ -z $PORT ]
then
    PORT=3306
fi

sed -i "s/USER_PROD/${USERNAME}/g"     LostAndFound/settings.py
sed -i "s/PASSWORD_PROD/${PASSWORD}/g" LostAndFound/settings.py
sed -i "s/HOST_PROD/${SQL_HOST}/g"     LostAndFound/settings.py 
sed -i "s/NAME_PROD/${DB_NAME}/g"      LostAndFound/settings.py
sed -i "s/PORT_PROD/${PORT}/g"         LostAndFound/settings.py


# ------- should be removed --------
#sed -i '/destructive_warning/s/True/False/g' ~/.myclirc
#echo 'DROP TABLE item_item' | python manage.py dbshell 
#echo 'DROP TABLE user_user' | python manage.py dbshell 
python manage.py makemigrations item
python manage.py makemigrations user
python manage.py migrate
# ------------------

exec "$@"

