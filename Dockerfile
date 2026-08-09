FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "demo:app", "--host", "0.0.0.0", "--port", "3000"]
