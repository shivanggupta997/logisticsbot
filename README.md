# 🚛 LogisticsBot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**LogisticsBot** is an AI-powered chatbot platform tailored for the logistics and supply chain industry. Built with **Django** and **Python**, it helps automate customer interactions, track shipments, and provide real-time responses to logistics queries.

---

## 🌟 Features

LogisticsBot provides a conversational interface to handle tasks such as:

-   📦 **Shipment Tracking:** Allow users to get real-time updates on their shipments.
-   📋 **Order Status Queries:** Provide instant information about order statuses.
-   📞 **Customer Support Automation:** Reduce manual effort by automating common customer queries.
-   📊 **Integration with Logistics Systems:** Designed to be extensible for integration with backend logistics APIs and databases.
-   🤖 **AI-Powered Conversations:** (Optional) Can be integrated with AI services like OpenAI to provide more natural and intelligent responses.

Ideal for companies looking to enhance customer experience and scale their support operations efficiently.

---

## 🧰 Tech Stack

-   **Programming Language:** 🐍 Python 3.13
-   **Web Framework:** 🌐 Django
-   **Containerization:** 🐳 Docker
-   **CI/CD:** ⚙️ Jenkins
-   **AI/NLP (Optional):** Integration capabilities for OpenAI API or other similar services.
-   **Database (Default Django):** SQLite (easily configurable to PostgreSQL, MySQL, etc.)

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

-   Git
-   Python 3.13 (or the version specified in your project)
-   pip (Python package installer)
-   Docker (for containerized deployment)
-   (Optional) A virtual environment tool like `venv` or `conda`.

### 1. Local Development (Without Docker)

Follow these steps to run the application on your local machine:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/shivanggupta997/logisticsbot.git
    cd logisticsbot
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    # venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install django dotenv google.generativeai gunicorn
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will typically be available at `http://127.0.0.1:8000/`.

### 2. Running with Docker

This project is Dockerized and can be run easily as a container.

#### Option A: Using the Pre-built Docker Image from Docker Hub

You can pull and run the pre-built image directly from Docker Hub:

1.  **Pull the image:**
    ```bash
    docker pull darksmiley1907/ailogibot:latest
    ```
    *(Note: Using `:latest` is common, but you can specify a version tag if available.)*

2.  **Run the container:**
    The application inside the container is configured to run on port 80.
    ```bash
    docker run -d -p 80:80 --name logisticsbot_container darksmiley1907/ailogibot:latest
    ```
    -   `-d`: Run in detached mode.
    -   `-p 80:80`: Map port 80 of the host to port 80 of the container.
    -   `--name logisticsbot_container`: Assign a name to the container for easier management.

3.  **Access the application:**
    Open your browser and navigate to `http://localhost/` (or `http://<your-docker-host-ip>/` if not running locally).

#### Option B: Building and Running the Docker Image from Source

If you want to build the image yourself:

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone https://github.com/shivanggupta997/logisticsbot.git
    cd logisticsbot
    ```

2.  **Build the Docker image:**
    This command uses the `Dockerfile` in the current directory.
    ```bash
    docker build -t logisticsbot-local .
    ```
    *(You can use `darksmiley1907/ailogibot` as the tag if you plan to push it to your Docker Hub).*

3.  **Run the container from your local build:**
    ```bash
    docker run -d -p 80:80 --name logisticsbot_container logisticsbot-local
    ```

4.  **Access the application:**
    Open your browser and navigate to `http://localhost/`.

---

## 🐳 Docker Hub Image

The official pre-built Docker image for this project is available on Docker Hub:

**Image:** `darksmiley1907/ailogibot`

**Link:** [https://hub.docker.com/repository/docker/darksmiley1907/ailogibot](https://hub.docker.com/repository/docker/darksmiley1907/ailogibot)

You can pull it using:
```bash
docker pull darksmiley1907/ailogibot:latest
