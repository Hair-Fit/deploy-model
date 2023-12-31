FROM python:3.8.10

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

RUN python3 init-model.py

RUN rm serviceaccount.json
RUN rm .env

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "main:app"]
