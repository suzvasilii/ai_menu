FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "fastapi[standard]"
COPY app /app/src
RUN mkdir /app/uploads
CMD ["fastapi", "run", "/app/src/main.py"]
