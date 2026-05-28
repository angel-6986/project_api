# Hardware-to-Cloud Sensor API

## Description
This project is a scalable, "full-loop" backend system designed to bridge hardware-level telemetry with cloud-based storage. It simulates an Industrial IoT (IIoT) architecture where edge devices (such as ESP32 microcontrollers) collect environmental sensor data and transmit it via a REST API to a secure, persistent database.

This project demonstrates the transition from a local development environment to a production-grade cloud deployment, utilizing modern industry best practices for data validation, database abstraction, and scalable architecture.

## Tech Stack
* **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Chosen for high performance and automatic documentation).
* **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) (Abstracts database interactions, allowing for seamless transition from SQLite to PostgreSQL).
* **Database**: PostgreSQL (Cloud/Production), SQLite (Local/Development).
* **Data Validation**: [Pydantic](https://docs.pydantic.dev/) (Ensures incoming sensor data meets strict type requirements).
* **Deployment**: [Render](https://render.com/) (PaaS for CI/CD and cloud hosting).
* **Infrastructure**: Python virtual environments (venv), Git, and WSL2 (Linux).

## Features
* **RESTful API**: Implements standard HTTP methods (`POST` for data ingestion, `GET` for data retrieval).
* **Scalable Architecture**: Uses an Object-Relational Mapper (ORM) to handle database schemas, facilitating scaling from local SQLite files to production-grade PostgreSQL.
* **Data Integrity**: Implements Pydantic models for strict JSON validation, preventing corrupted data from entering the database.
* **Environment-Aware Configuration**: Automatically detects if the API is running locally or in a cloud environment to switch between SQLite and PostgreSQL.

## Getting Started

### Prerequisites
* Python 3.10+
* Virtual Environment (venv) configured

### Local Setup
1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd project_api
    ```
2.  **Activate your virtual environment**:
    ```bash
    source venv/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Server**:
    ```bash
    uvicorn server.server:app --reload
    ```
    ** Loadable through render website **

5.  **Run the Hardware Simulator**:
    ```bash
    python hardware/sensor.py
    ```

## API Documentation
Once the server is running, you can access the interactive Swagger UI dashboard at `https://project-api-am.onrender.com/docs` to test endpoints and interact with the data model directly.