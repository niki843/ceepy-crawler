
# **FastAPI Screenshot Crawler**

A simple web crawler built with **FastAPI**, **Playwright**, and **PostgreSQL**. This app takes screenshots of webpages and stores their file paths in a PostgreSQL database. It supports the following functionality:

1. Take a screenshot of a webpage and save the file path in the database.
2. Retrieve the screenshot file path from the database by ID.

## **Features**
- Web scraping and screenshot capture using **Playwright**.
- Store and manage screenshot file paths in a **PostgreSQL** database.
- Easy to test and develop with **Docker**.

---

## **Technologies**
- **FastAPI**: Web framework for building APIs.
- **Playwright**: Headless browser automation for web scraping and screenshot capture.
- **PostgreSQL**: Relational database to store file paths.
- **SQLAlchemy**: ORM for database interaction.
- **Docker**: Containerization for easy testing and deployment.
- **Alembic**: Database migrations for schema management.

---

## **Getting Started**

### **Prerequisites**
Make sure you have **Docker** and **docker-compose** installed.  
You also need Python 3.10+ to run locally.

---

### **Setting Up the Application**

1. **Clone the repository**:
   ```sh
   git clone https://github.com/niki843/creepy-crawler.git
   cd creepy-crawler
   ```

2. **Create and start the Docker containers**:
   The `docker-compose.yml` file sets up PostgreSQL and the application container.

   ```sh
   docker-compose up -d
   ```

---

## **Endpoints**

### **1. Save a Screenshot Path**

- **Endpoint**: `POST /screenshot`
- **Description**: Takes a screenshot and stores its path in the database.
- **Request Body**:
    ```json
    {
      "start_url": "https://example.com/"
      "links_to_follow_amount": 4
    }
    ```
- **Response**:
    ```json
    {
      "id": 1
    }
    ```

### **2. Get Screenshot by ID**

- **Endpoint**: `GET /screenshot/{file_id}`
- **Description**: Retrieves the stored screenshot image by the screenshot ID.
#### **Response**:
- **Status Code**: `200 OK`
- **Content-Type**: `image/png` (or `image/jpeg`)
- **Body**: The raw image data (screenshot).

---

## **Docker Compose Configuration**

The `docker-compose.yml` file contains the following services:

- **db**: PostgreSQL database.
- **app**: FastAPI application (with Playwright for crawling).

To start both services together, run:
```sh
docker-compose up -d
```

- **PostgreSQL** is configured with the username `postgres`, password `password`, and database `postgres`.
- The app is accessible on `http://localhost:8000`.

---

## **Development**

### **Building the Docker Image**  
If you want to rebuild the Docker container, use:
```sh
docker-compose build
```

### **Viewing Logs**
To view logs from the app container:
```sh
docker-compose logs -f app
```

### **Stopping Docker Containers**
To stop the app and database containers:
```sh
docker-compose down
```

---

## **Testing Locally**

If you prefer testing without Docker, you can run the app directly on your machine:

1. **Set up a local PostgreSQL instance**.
2. **Configure your `.env`** file to point to your local database (optional):
    ```ini
    DATABASE_URL=postgresql+asyncpg://myuser:mypassword@localhost/mydatabase
    ```

3. **Start FastAPI locally**:
   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
