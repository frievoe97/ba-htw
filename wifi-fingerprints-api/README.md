# WiFi-Fingerprints API

## Overview

This project is a web application that uses a FastAPI backend, a MariaDB database, and monitoring tools like Prometheus and Grafana. The entire stack is containerized using Docker and can be easily started using Docker Compose.

## Prerequisites

Before starting, ensure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Environment Variables

You need to set up the following environment variables in a `.env` file in the project root:

```
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=your_database_name
MYSQL_USER=your_database_user
MYSQL_PASSWORD=your_user_password
```

## Starting the Project

1. **Clone the repository** to your local machine.

2. **Navigate to the project directory**:

```
cd /path/to/your/project
```

3. **Create a `.env` file** in the root of the project directory with the required environment variables as specified above.

4. **Start the application** using Docker Compose:

```
docker-compose up --build
```

This will build the Docker images and start the services defined in the `docker-compose.yml` file.

5. **Access the application**:

   - The FastAPI application will be available at: [http://localhost:8000](http://localhost:8000)
   - The Prometheus monitoring tool will be accessible at: [http://localhost:9090](http://localhost:9090)
   - The Grafana dashboard will be accessible at: [http://localhost:3000](http://localhost:3000)

## Services

### Web (FastAPI)

- **Build Context:** `./app`
- **Dockerfile:** `Dockerfile` located in the `./app` directory
- **Command:** `uvicorn main:app --host 0.0.0.0 --port 8000`
- **Ports:** `8000:8000`
- **Environment:** `DATABASE_URL` configured for connection to MariaDB

### Database (MariaDB)

- **Image:** `mariadb:latest`
- **Ports:** `3307:3306` (Host:Container)
- **Volumes:** `db_data:/var/lib/mysql`
- **Healthcheck:** MariaDB health check to ensure the service is ready

### Prometheus

- **Image:** `prom/prometheus`
- **Ports:** `9090:9090`
- **Volumes:** Mounts for configuration and data persistence

### Grafana

- **Image:** `grafana/grafana`
- **Ports:** `3000:3000`
- **Volumes:** `grafana_data:/var/lib/grafana`

## Stopping the Project

To stop the application, run:

```
docker-compose down
```

This will stop and remove all the containers, but the volumes will be preserved, so your data is safe.

## Cleanup

If you want to remove all containers, networks, and volumes, you can use:

```
docker-compose down -v
```

This will also remove the persistent data stored in the volumes.

## Additional Notes

- Ensure that any changes to the environment variables are reflected in your `.env` file before restarting the containers.
- The `prometheus_data` folder is ignored by Git except for its structure, allowing Prometheus to store its data without being tracked by version control.

## Troubleshooting

- If you encounter issues with the containers not starting properly, check the logs using:

```
docker-compose logs
```

- Ensure that the environment variables in your `.env` file are correctly set up.
