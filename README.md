# Task Manager API

## Description
A backend service built with FastAPI for managing tasks. It includes user authentication, stores data in PostgreSQL, uses Redis for caching, and runs in Docker containers for easy setup.
## Table of Contents
- [Description](#description)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Task Management](#task-management)

## Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1. **Clone the repository**
    ```bash
    git clone https://github.com/MaksimSergin/Task-Manager-FastAPI-Example.git
    cd Task-Manager-FastAPI-Example
    ```

2. **Configure Environment**
   Copy `.env.sample` to `.env`:
    ```bash
    cp .env.sample .env
    ```

## Running the Application
To start the application:

1. **Start Services**
    ```bash
    docker-compose up --build
    ```
   - The service will be accessible at `http://localhost:8000/`.
2. **Health Check**
    - Access the health endpoint to ensure the app is running:
        - [http://localhost:8000/health](http://localhost:8000/health)


## API Endpoints

### Authentication
- **Register User**
  - **URL:** `/api/v1/auth/register`
  - **Method:** `POST`
  - **Request Body:**
    ```json
    {
      "username": "testuser",
      "password": "password123"
    }
    ```
  - **Response:**
    ```json
    {
      "id": 1,
      "username": "testuser"
    }
    ```

- **Login**
  - **URL:** `/api/v1/auth/login`
  - **Method:** `POST`
  - **Request Body:**
    ```json
    {
      "username": "testuser",
      "password": "password123"
    }
    ```
  - **Response:**
    ```json
    {
      "access_token": "jwt_access_token",
      "refresh_token": "jwt_refresh_token",
      "token_type": "bearer"
    }
    ```

- **Refresh Token**
  - **URL:** `/api/v1/auth/refresh`
  - **Method:** `POST`
  - **Request Body:**
    ```json
    {
      "refresh_token": "jwt_refresh_token"
    }
    ```
  - **Response:**
    ```json
    {
      "access_token": "new_jwt_access_token",
      "refresh_token": "new_jwt_refresh_token",
      "token_type": "bearer"
    }
    ```

### Task Management
- **Create Task**
  - **URL:** `/api/v1/tasks/`
  - **Method:** `POST`
  - **Headers:** `Authorization: Bearer <access_token>`
  - **Request Body:**
    ```json
    {
      "title": "New Task",
      "description": "Details of the task",
      "status": "in_progress"
    }
    ```
  - **Response:**
    ```json
    {
      "id": 1,
      "title": "New Task",
      "description": "Details of the task",
      "status": "in_progress",
      "user_id": 1
    }
    ```

- **Get Tasks**
  - **URL:** `/api/v1/tasks/`
  - **Method:** `GET`
  - **Headers:** `Authorization: Bearer <access_token>`
  - **Query Parameters (optional):** `status` (e.g., `in_progress`, `completed`)
  - **Response:**
    ```json
    [
      {
        "id": 1,
        "title": "New Task",
        "description": "Details of the task",
        "status": "in_progress",
        "user_id": 1
      }
    ]
    ```

- **Update Task**
  - **URL:** `/api/v1/tasks/{task_id}`
  - **Method:** `PUT`
  - **Headers:** `Authorization: Bearer <access_token>`
  - **Request Body:**
    ```json
    {
      "title": "Updated Task Title",
      "description": "Updated description",
      "status": "completed"
    }
    ```
  - **Response:**
    ```json
    {
      "id": 1,
      "title": "Updated Task Title",
      "description": "Updated description",
      "status": "completed",
      "user_id": 1
    }
    ```

- **Delete Task**
  - **URL:** `/api/v1/tasks/{task_id}`
  - **Method:** `DELETE`
  - **Headers:** `Authorization: Bearer <access_token>`
  - **Response:** No content (204 status code)

