@echo off

echo Creating ClinicCore project structure...

mkdir app
mkdir app\core
mkdir app\models
mkdir app\schemas
mkdir app\routers
mkdir app\services
mkdir app\repositories
mkdir app\templates
mkdir app\static
mkdir app\plugins

mkdir tests

mkdir HELP

(
echo # Installation Guide
) > HELP\INSTALL.txt

(
echo # Run Guide
) > HELP\RUN.txt

(
echo # Architecture Documentation
) > HELP\ARCHITECTURE.txt

(
echo # Database Design
) > HELP\DATABASE.txt

(
echo # Development Roadmap
) > HELP\ROADMAP.txt

(
echo # Architecture Decisions
) > HELP\DECISIONS.txt


(
echo from fastapi import FastAPI
echo.
echo app = FastAPI^(
echo     title="ClinicCore"
echo ^)
echo.
echo @app.get^("/"^)
echo def home^(^):
echo     return {"status": "ClinicCore running"}
) > main.py


(
echo # ClinicCore environment configuration
echo DATABASE_URL=
echo SECRET_KEY=
) > .env.example


(
echo [build-system]
echo requires = ["setuptools", "wheel"]
echo build-backend = "setuptools.build_meta"
echo.
echo [project]
echo name = "cliniccore"
echo version = "0.1.0"
echo description = "Clinic Management Platform"
echo requires-python = ">=3.12"
) > pyproject.toml


echo.
echo Project structure created successfully.
tree /F

pause