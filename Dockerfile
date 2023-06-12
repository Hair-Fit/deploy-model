FROM python:3.8.10

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

RUN python3 init-model.py

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "main:app"]