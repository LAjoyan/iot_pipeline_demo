FROM python:3.13-slim

WORKDIR /app
COPY consumer.py /app/
COPY pyproject.toml /app/

RUN pip install --no-cache-dir uv
RUN uv sync --no-dev

CMD [ "uv", "run", "consumer.py" ]