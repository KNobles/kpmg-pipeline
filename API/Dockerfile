# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10

RUN mkdir /app
WORKDIR /app
COPY . /app

EXPOSE 8080

# Install pip requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


CMD [ "uvicorn", "app:app", "--host=0.0.0.0", "--reload" ]