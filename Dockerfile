FROM python:3.11-slim AS base

ARG USERNAME=appuser
ARG UID=1000
ARG GID=1000
RUN addgroup --gid $GID $USERNAME \
    && adduser --uid $UID --gid $GID --disabled-password --gecos "" $USERNAME

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
RUN chown $USERNAME:$USERNAME /app

COPY --chown=$USERNAME:$USERNAME requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=$USERNAME:$USERNAME . .

ENV GROQ_API_KEY=""
ENV OPENROUTER_API_KEY=""

EXPOSE 8000
USER $USERNAME

CMD python3 smart_router.py & uvicorn web_ui:app --host 0.0.0.0 --port 8000
