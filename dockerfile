FROM python:3.13-slim

EXPOSE 8000

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN rm -f -- team.json

CMD ["uvicorn", "src.main:app", "--port", "8000", "--host", "0.0.0.0"]
