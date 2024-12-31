<!-- # Setup environment:

python3 -m venv venv
source venv/bin/activate  
# On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

or
docker-compose up -d --build

docker-compose logs -f backend
 -->

# Reverse Image Lookup

Reverse Image Lookup is a full-stack application that allows users to upload an image and find similar faces from a database. The project leverages modern web technologies for the frontend and a robust backend infrastructure to handle image processing, storage, and search functionalities.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Client Setup](#client-setup)
  - [Server Setup](#server-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Image Upload**: Users can upload images containing faces.
- **Face Detection & Embedding**: Utilizes machine learning models to detect faces and generate embeddings.
- **Search Similar Faces**: Finds and displays similar faces from the database based on embedding vectors.
- **Responsive UI**: Built with React and Tailwind CSS for a seamless user experience.
- **Scalable Backend**: FastAPI backend with MongoDB and Redis for efficient data storage and retrieval.
- **Dockerized Deployment**: Easy setup and deployment using Docker and Docker Compose.

## Technologies Used

### Frontend

- **Vite**: Fast frontend build tool.
- **React**: JavaScript library for building user interfaces.
- **Tailwind CSS**: Utility-first CSS framework for styling.
- **Lucide React**: Icon library.
- **ESLint**: Linting utility for code quality.

### Backend

- **FastAPI**: High-performance web framework for building APIs.
- **Python**: Programming language for backend logic.
- **MongoDB**: NoSQL database for storing image data.
- **Redis**: In-memory data structure store for vector similarity search.
- **Docker**: Containerization platform.
- **Uvicorn**: ASGI server for running FastAPI applications.
- **Facenet-PyTorch**: Deep learning models for face detection and recognition.

## Prerequisites

- **Node.js** (v14 or later)
- **npm** or **yarn**
- **Docker** and **Docker Compose**
- **Python** (v3.8 or later)
- **MongoDB** and **Redis** (if not using Docker)

## Installation

### Client Setup

1. **Navigate to the client directory:**

   ```bash
   cd Reverse\ image\ lookup/client
   ```

2. **Install dependencies:**

   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure Environment Variables:**

   If there are any environment variables required for the client, create a `.env` file based on a provided template (if available).

4. **Start the Development Server:**

   ```bash
   npm run dev
   # or
   yarn dev
   ```

   The client will be available at `http://localhost:5173`.

### Server Setup

There are two ways to set up the server: using Docker or setting it up manually.

#### Using Docker

1. **Navigate to the server directory:**

   ```bash
   cd Reverse\ image\ lookup/server
   ```

2. **Create a `.env` file:**

   Ensure the `.env` file has the correct configurations. Modify the `MONGODB_URL` if necessary.

3. **Build and Run Containers:**

   ```bash
   docker-compose up --build
   ```

   This command will build the backend image and start both the backend and Redis services.

4. **Access the Backend:**

   The FastAPI server will be running at `http://localhost:8000`.

#### Manual Setup

1. **Navigate to the server directory:**

   ```bash
   cd Reverse\ image\ lookup/server
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**

   Ensure the `.env` file is properly configured with the correct MongoDB and Redis URLs.

5. **Start MongoDB and Redis:**

   - **MongoDB:** [Installation Guide](https://docs.mongodb.com/manual/installation/)
   - **Redis:** [Installation Guide](https://redis.io/download)

6. **Run the FastAPI Server:**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

   The backend will be accessible at `http://localhost:8000`.

## Running the Application

1. **Start the Backend:**

   Ensure the backend server is running either via Docker or manually as described above.

2. **Start the Frontend:**

   Ensure the frontend development server is running.

3. **Access the Application:**

   Open your browser and navigate to `http://localhost:5173` to use the Reverse Image Lookup tool.

## API Endpoints

### `POST /api/search`

**Description:** Upload an image to search for similar faces.

**Request:**

- **Headers:**
  - `Content-Type: multipart/form-data`

- **Body:**
  - `file`: Image file (PNG, JPG, WEBP)

**Response:**

- **Status Code:** `200 OK`
- **Body:** JSON array of matching images with similarity scores.

  ```json
  [
    {
      "url": "https://example.com/face1.jpg",
      "source_url": "https://example.com/profile1",
      "similarity": 95.5
    },
    {
      "url": "https://example.com/face2.jpg",
      "source_url": "https://example.com/profile2",
      "similarity": 89.3
    }
    // More results...
  ]
  ```

**Error Responses:**

- `400 Bad Request`: Invalid image file or no face detected.
- `500 Internal Server Error`: Server-side error during processing.

