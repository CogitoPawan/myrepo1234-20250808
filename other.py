.
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── anomaly_detector.py
│   └── utils.py
├── notification_service
│   ├── __init__.py
│   └── main.py
├── tests
│   ├── test_anomaly_detection.py
│   └── test_views.py
├── config.py
├── Dockerfile
├── docker-compose.yaml
├── README.md
├── requirements.txt
└── .github
    └── workflows
        └── ci-cd.yaml

FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:password@db/salesdb
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: salesdb
    ports:
      - "5432:5432"

  notification_service:
    image: notification_service
    build:
      context: ./notification_service
      dockerfile: Dockerfile
    ports:
      - "8000:8000"

1. Clone the repository:

2. Start all services using Docker Compose:

To run unit tests:

Flask==2.0.1
SQLAlchemy==1.4.22
psycopg2-binary==2.9.1
scikit-learn==0.24.2
requests==2.25.1
fastapi==0.65.2
uvicorn==0.13.4
pytest==6.2.4

name: CI/CD Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest
    
    - name: Build Docker image
      run: |
        docker-compose build

    - name: Deploy to Kubernetes
      run: |
        echo "Deployment step goes here"