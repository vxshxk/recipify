FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/
RUN apt-get update && apt-get install libgl1 libglib2.0 -y
RUN python -m pip install -r requirements.txt
COPY . /app/
RUN python /app/recipify/manage.py migrate
EXPOSE 8000
ENTRYPOINT [ "python", "/app/recipify/manage.py", "runserver", "0.0.0.0:8000" ]