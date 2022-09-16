FROM python:3.10

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY data data
COPY start start
COPY static static
COPY templates templates

CMD flask run -h 0.0.0.0 -p 80