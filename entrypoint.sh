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


exec "$@"


