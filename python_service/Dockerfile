FROM python:3.8-slim-buster
RUN pip install --upgrade pip

WORKDIR /src
COPY ./src /src
# Install dependencies:
COPY requirements.txt .
COPY .env .
RUN pip install -r requirements.txt
EXPOSE 3001
COPY /src/app.py .
# Run the application:
#CMD gunicorn --bind 0.0.0.0:3001 app:app
CMD python app.py