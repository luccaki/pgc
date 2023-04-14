FROM python:3.8-slim-buster
RUN pip install --upgrade pip

WORKDIR /src
COPY ./src /src
# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 3001
COPY /src/app.py .
# Run the application:
CMD python app.py