FROM python:3.6

WORKDIR /usr/src/app

COPY . ./
RUN pip install --no-cache-dir -r requirements.txt
RUN rm LostAndFound/settings.py && mv LostAndFound/settings_prod.py LostAndFound/settings.py
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
CMD ["python" , "./manage.py", "runserver", "0.0.0.0:8000"]


