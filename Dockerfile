FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn httpx pydantic requests
RUN chmod +x start.sh
EXPOSE 8000
CMD ["./start.sh"]
