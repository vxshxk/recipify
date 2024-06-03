FROM python:3.9-alpine
WORKDIR /app
COPY . /app/
RUN python -m pip install -r requirements.txt
RUN cd /app/recipify/ && python manage.py migrate
EXPOSE 8000
ENTRYPOINT [ "python", "/app/recipify/manage.py", "runserver", "0.0.0.0:8000" ]