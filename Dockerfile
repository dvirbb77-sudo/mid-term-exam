FROM python:3.12-slim
SHELL ["/bin/bash", "-c"]
ENV POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false
        
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get purge -y --auto-remove curl \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="$POETRY_HOME/bin:$PATH"
RUN groupadd -r devops && useradd -r -g devops -u 1001 appuser
WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --only main
COPY app.py .
RUN chown -R appuser:devops /app
USER appuser
EXPOSE 5000
CMD ["python", "app.py"]