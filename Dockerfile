FROM python:3.10
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir flask  requests flask_sqlalchemy flask_bcrypt
CMD python3 main.py