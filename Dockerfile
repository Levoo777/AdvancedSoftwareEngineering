FROM python:3.10
 
WORKDIR /app
 
COPY requirements.txt ./
 
RUN pip install -r requirements.txt
 
COPY . .
 
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

CMD ["python3", "-m", "flask", "run"]