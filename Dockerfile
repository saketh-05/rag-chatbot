FROM python:3.11-slim
WORKDIR /
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["uvicorn", "chatbot:app", "--host", "0.0.0.0", "--port", "8080"]