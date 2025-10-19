# Setup and Installation Guide

This document provides detailed instructions for setting up and running the IoT Analytics Platform in a local development environment.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Configuration](#environment-configuration)
3. [Running with Docker Compose](#running-with-docker-compose)
4. [Accessing the Application](#accessing-the-application)
5. [Development Workflow](#development-workflow)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following tools installed on your system:

### Required Tools

- **Docker**: Container runtime for running services
  - [Installation Guide](https://docs.docker.com/get-docker/)
  - Verify installation: `docker --version`

- **Docker Compose**: Tool for defining and running multi-container applications
  - [Installation Guide](https://docs.docker.com/compose/install/)
  - Verify installation: `docker-compose --version`

- **Git**: Version control system
  - [Installation Guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
  - Verify installation: `git --version`

### System Requirements

- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: At least 5GB free
- **OS**: Linux, macOS, or Windows (with WSL2)

## Environment Configuration

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd iot-analytics-platform
```

### Step 2: Configure Backend Environment

Create a `.env` file in the `backend` directory:

```bash
cp backend/.env.example backend/.env
```

The default configuration is suitable for local development:

```ini
# backend/.env
DATABASE_URL=postgresql://user:password@postgres:5432/iot_analytics_db
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
LOG_LEVEL=INFO
```

**Important**: For production deployments, change the `SECRET_KEY` to a strong, random value.

### Step 3: Configure Frontend Environment

Create a `.env.local` file in the `frontend` directory:

```bash
cp frontend/.env.example frontend/.env.local
```

The default configuration:

```ini
# frontend/.env.local
VITE_API_URL=http://localhost:8000
```

This tells the frontend where to find the backend API. For production, update this to your production API URL.

## Running with Docker Compose

### Starting the Application

The simplest way to run the entire application is with Docker Compose:

```bash
docker-compose up --build
```

**What this command does:**
- Builds Docker images for backend and frontend
- Creates and starts containers for PostgreSQL, backend, and frontend
- Sets up networking between services
- Displays logs from all services

**Expected output:**
```
Creating network "iot_analytics_network" with default driver
Creating iot_analytics_db ... done
Creating iot_analytics_api ... done
Creating iot_analytics_frontend ... done
```

### Running in Background

To run services in the background:

```bash
docker-compose up -d --build
```

Check the status:
```bash
docker-compose ps
```

View logs:
```bash
docker-compose logs -f
```

### Stopping the Application

```bash
docker-compose down
```

To also remove data volumes:
```bash
docker-compose down -v
```

## Accessing the Application

Once all services are running, access them via:

### Frontend Dashboard
- **URL**: http://localhost:3000
- **Description**: Interactive IoT Analytics Dashboard
- **Features**: Device management, alert viewing, data visualization

### Backend API
- **Base URL**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

### API Documentation

#### Swagger UI (Interactive)
- **URL**: http://localhost:8000/docs
- **Features**: Test endpoints directly, view request/response schemas

#### ReDoc (Alternative)
- **URL**: http://localhost:8000/redoc
- **Features**: Clean, searchable API documentation

### Database
- **Host**: localhost
- **Port**: 5432
- **Username**: user
- **Password**: password
- **Database**: iot_analytics_db

## Development Workflow

### Backend Development

#### Accessing Backend Container

```bash
docker-compose exec backend /bin/bash
```

#### Running Tests

```bash
docker-compose exec backend pytest
```

Run tests with coverage:
```bash
docker-compose exec backend pytest --cov=app
```

#### Code Formatting

Format code with Black:
```bash
docker-compose exec backend black app/
```

Sort imports:
```bash
docker-compose exec backend isort app/
```

Lint code:
```bash
docker-compose exec backend flake8 app/
```

#### Viewing Logs

```bash
docker-compose logs backend
```

Follow logs in real-time:
```bash
docker-compose logs -f backend
```

### Frontend Development

#### Accessing Frontend Container

```bash
docker-compose exec frontend sh
```

#### Running Tests

```bash
docker-compose exec frontend npm test
```

#### Code Formatting

```bash
docker-compose exec frontend npm run format
```

#### Type Checking

```bash
docker-compose exec frontend npm run type-check
```

#### Building for Production

```bash
docker-compose exec frontend npm run build
```

#### Viewing Logs

```bash
docker-compose logs frontend
```

### Database Management

#### Accessing PostgreSQL

```bash
docker-compose exec postgres psql -U user -d iot_analytics_db
```

#### Useful SQL Commands

List all tables:
```sql
\dt
```

View table structure:
```sql
\d devices
```

Count records:
```sql
SELECT COUNT(*) FROM devices;
```

#### Database Backup

```bash
docker-compose exec postgres pg_dump -U user iot_analytics_db > backup.sql
```

#### Database Restore

```bash
docker-compose exec postgres psql -U user iot_analytics_db < backup.sql
```

## Making Changes

### Backend Changes

1. Edit Python files in the `backend/app` directory
2. The application automatically reloads due to the `--reload` flag in docker-compose.yml
3. Check logs for any errors: `docker-compose logs backend`

### Frontend Changes

1. Edit React/TypeScript files in the `frontend/src` directory
2. The development server automatically recompiles
3. Refresh your browser to see changes

### Database Schema Changes

For production migrations, use Alembic:

```bash
docker-compose exec backend alembic revision --autogenerate -m "Description of changes"
docker-compose exec backend alembic upgrade head
```

## Troubleshooting

### Common Issues

#### Port Already in Use

**Error**: `Address already in use`

**Solution**: Change port mappings in `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # Change frontend port
  - "8001:8000"  # Change backend port
  - "5433:5432"  # Change database port
```

#### Container Won't Start

**Solution**: Check logs for errors:
```bash
docker-compose logs <service-name>
```

#### Database Connection Failed

**Solution**: Verify database is healthy:
```bash
docker-compose ps
```

Wait for database to be ready (check health status) before starting backend.

#### Frontend Can't Connect to Backend

**Cause**: API URL misconfiguration

**Solution**: 
1. Verify `VITE_API_URL` in `frontend/.env.local`
2. Ensure backend is running: `docker-compose logs backend`
3. Test API directly: `curl http://localhost:8000/health`

#### Docker Build Fails

**Solution**: Clear Docker cache and rebuild:
```bash
docker-compose down
docker system prune -a
docker-compose up --build
```

### Performance Issues

#### Slow Container Startup

- Increase Docker memory allocation
- Check system resources: `docker stats`

#### High Memory Usage

- Reduce database connection pool size in `backend/app/database.py`
- Clear Docker cache: `docker system prune`

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Create test data**: Use the API to create devices and alerts
3. **View dashboard**: Check http://localhost:3000
4. **Review code**: Examine the project structure
5. **Run tests**: Execute `docker-compose exec backend pytest`

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)

## Support

For issues or questions:
1. Check this guide's troubleshooting section
2. Review Docker logs: `docker-compose logs`
3. Consult project documentation
4. Check the README.md for additional information
