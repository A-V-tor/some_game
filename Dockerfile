FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install poetry

RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "python", "main.py"]