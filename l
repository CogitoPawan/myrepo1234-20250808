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