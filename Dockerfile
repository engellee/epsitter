FROM python:3
EXPOSE 8989/tcp
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/* ./
CMD [ "python3", "/app/sitter.py", "/app/sitter.yaml" ]
