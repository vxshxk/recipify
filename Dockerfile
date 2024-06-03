FROM python:3.11-bullseye
WORKDIR /app
COPY requirements.txt /app/
RUN python -m pip install -r requirements.txt
COPY . /app/
RUN cd /app/recipify/ && python manage.py migrate
EXPOSE 8000
ENTRYPOINT [ "python", "/app/recipify/manage.py", "runserver", "0.0.0.0:8000" ]