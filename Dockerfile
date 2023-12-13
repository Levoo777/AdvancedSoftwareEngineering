FROM python:3.10
 
WORKDIR /app
 
COPY requirements.txt ./
 
RUN pip install -r requirements.txt
 
COPY . .
 
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

COPY /database/kundendatenbank.sql /app/database/kundendatenbank.sql

VOLUME /app/database

EXPOSE 5000

CMD ["python3", "-m", "flask", "run"]