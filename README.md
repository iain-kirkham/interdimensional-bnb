🌌 Interdimensional B&B

A Django-based booking platform for travelers across the multiverse. Manage listings, reality rules, and cross-dimensional reservations.


# 🛠 Tech Stack

- Language: Python 3.12 (via uv)
- Database: PostgreSQL 15
- Containerisation: Docker & Docker Compose

1. Clone & Setup Environment

```bash
git clone https://github.com/iain-kirkham/interdimensional-bnb.git
cd interdimensional-bnb
cp .env.example .env
```

2. Launch Containers

This will build the web image and pull the Postgres database.

```bash
docker-compose up --build
```

The site will be live at: `http://localhost:8000`

3. Initialise Database

In a new terminal, run the migrations and create your admin account:

```bash
# Run migrations
docker-compose exec web uv run python manage.py migrate

# Create your superuser
docker-compose exec web uv run python manage.py createsuperuser
```

# 📦 Dependency Management

We use uv for lightning-fast dependency management. Because of our Docker volume mapping, changes sync both ways.

Add a new package:
```bash
    docker-compose exec web uv add <package-name>
```

Sync environment (if a teammate added a package):

```bash
docker-compose exec web uv sync
```


# Command cheat sheet

```bash
# Services
docker compose up                 # Build and start services
docker compose up --build         # Force rebuild
docker compose down               # Stop and remove containers
docker compose down -v            # Stop and remove containers + volumes (wipe DB)

# Django management (runs inside the web container via `uv`)
docker compose exec web uv run python manage.py migrate
docker compose exec web uv run python manage.py makemigrations
docker compose exec web uv run python manage.py createsuperuser
docker compose exec web uv run python manage.py shell

# Development helpers
docker compose exec web uv run python manage.py runserver 0.0.0.0:8000
docker compose exec web uv run python manage.py collectstatic --noinput

# Package management
docker compose exec web uv add <package>
docker compose exec web uv add --dev <package>
docker compose exec web uv remove <package>
docker compose exec web uv sync
```