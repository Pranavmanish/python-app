# SWE 645: Extra Credit – Student Survey Application

## Team Members

- Pranav Manish Reddi Madduri (G01504276) – RDS database setup and backend integration  
- Lavanya Jillella (G01449670) – CI/CD pipeline configuration and endpoint testing  
- Sneha Rathi (G01449688) – Kubernetes deployment via Rancher  
- Chennu Naga Venkata Sai (G01514409) – Docker container build and Docker Hub publishing  

## Project Overview

This project implements a Python-based student feedback form using Flask. It supports RESTful operations and integrates with a MySQL database hosted on Amazon RDS. The application is containerized with Docker, deployed on Kubernetes via Rancher, and delivered using a Jenkins-based CI/CD pipeline.

## Technologies Used

- Python 3.11 and Flask  
- SQLAlchemy ORM  
- MySQL on Amazon RDS  
- Docker  
- Kubernetes (via Rancher)  
- Jenkins and GitHub for CI/CD  
- Postman for testing  

## System Design Overview

- Flask app captures feedback using a form-based interface  
- SQLAlchemy manages ORM layer for database interaction  
- Application containerized using Docker  
- Jenkins pipeline automates build and deployment  
- Kubernetes YAML files define deployment and service specifications  
- Postman used for REST API testing with authentication  

## Step-by-Step Process

### 1. Design the Application
The app is structured to collect student feedback and store it in a remote MySQL database. It offers REST endpoints for both data insertion and retrieval.

### 2. Backend Logic
A Flask application is created and initialized using environment-based configurations. The SQLAlchemy ORM is used for defining and interacting with database tables.

### 3. Database Setup
An Amazon RDS MySQL instance is launched and connected to the Flask app. A table is created to store user feedback with fields for ID, name, and feedback message.

### 4. Dependency Management
Required Python libraries including Flask, SQLAlchemy, and PyMySQL are declared in a requirements file to ensure consistent environments during deployment.

### 5. Dockerization
A Dockerfile is created to package the Python application. The container is tested locally and then pushed to Docker Hub.

### 6. Kubernetes Deployment
Deployment and service specifications are written in YAML files. These are applied to a Kubernetes cluster via Rancher to create a scalable and load-balanced application deployment.

### 7. CI/CD Automation
A Jenkinsfile is written to automate code checkout, Docker image build and push, and Kubernetes deployment. Jenkins is configured with credentials and integrated with the GitHub repository.

### 8. API Testing
REST API endpoints are tested using Postman. Authorization tokens from Rancher are used to authenticate the requests. Feedback submissions and data retrieval are verified.


