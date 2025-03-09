# Makefile for setting up the environment, running Streamlit and FastAPI apps separately, and cleaning Docker

# Define variables
VENV_NAME = venv
DOCKER_COMPOSE_PATH = weatherchatbot/src/weatherchatbot
STREAMLIT_APP = streamlit_app.py
FASTAPI_APP = fastapi_app.py  # Update with the correct file name for your FastAPI app
PORT_STREAMLIT = 8501  # Default port for Streamlit
PORT_FASTAPI = 8000      # Default port for FastAPI
PYTHON_VERSION := 3.12.0
PYTHON_TARBALL := Python-$(PYTHON_VERSION).tgz
PYTHON_SRC_DIR := Python-$(PYTHON_VERSION)

# Install required development tools
install-dev-tools:
	@echo "Installing required development tools..."
	sudo apt update && sudo apt upgrade -y
	sudo apt install -y build-essential libffi-dev zlib1g-dev \
		libbz2-dev liblzma-dev wget libsqlite3-dev sqlite3

# Download and install Python
install-python:
	@echo "Downloading and installing Python $(PYTHON_VERSION)..."
	wget https://www.python.org/ftp/python/$(PYTHON_VERSION)/$(PYTHON_TARBALL)
	tar xzf $(PYTHON_TARBALL)
	cd $(PYTHON_SRC_DIR) && sudo ./configure --enable-optimizations
	cd $(PYTHON_SRC_DIR) && make
	cd $(PYTHON_SRC_DIR) && sudo make altinstall

# Create the virtual environment
create_venv:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_NAME)

# Install dependencies in the virtual environment
install_deps:
	@echo "Installing dependencies..."
	$(VENV_NAME)/bin/pip install -r requirements.txt

# Run Streamlit app
run_streamlit:
	@echo "Running Streamlit app..."
	$(VENV_NAME)/bin/streamlit run $(STREAMLIT_APP) --server.port $(PORT_STREAMLIT)

# Run FastAPI app
run_fastapi:
	@echo "Running FastAPI app..."
	$(VENV_NAME)/bin/uvicorn $(FASTAPI_APP):app --host 0.0.0.0 --port $(PORT_FASTAPI) --reload

# Clean up: Remove virtual environment
clean:
	@echo "Removing virtual environment..."
	rm -rf $(VENV_NAME)

# Run both Streamlit and FastAPI separately

# Run Streamlit only
run-streamlit-only: create_venv install_deps
	@echo "Running Streamlit app..."
	$(VENV_NAME)/bin/streamlit run $(STREAMLIT_APP) --server.port $(PORT_STREAMLIT)

# Run FastAPI only
run-fastapi-only: create_venv install_deps
	@echo "Running FastAPI app..."
	$(VENV_NAME)/bin/uvicorn $(FASTAPI_APP):app --host 0.0.0.0 --port $(PORT_FASTAPI) --reload

# Default target to run everything
all: create_venv install_deps run-streamlit-only run-fastapi-only

# Run both apps concurrently (this will run Streamlit and FastAPI together)
run_all: create_venv install_deps
	@echo "Running both Streamlit and FastAPI..."
	# Running both Streamlit and FastAPI simultaneously in the background
	$(VENV_NAME)/bin/streamlit run $(STREAMLIT_APP) --server.port $(PORT_STREAMLIT) & \
	$(VENV_NAME)/bin/uvicorn $(FASTAPI_APP):app --host 0.0.0.0 --port $(PORT_FASTAPI) --reload

# Build and run Docker Compose for both services
docker-compose-up:
	@echo "Building and running Docker Compose..."
	cd $(DOCKER_COMPOSE_PATH) && docker-compose up --build

# Stop and remove Docker Compose containers for both services
docker-compose-down:
	@echo "Stopping and removing Docker Compose containers..."
	cd $(DOCKER_COMPOSE_PATH) && docker-compose down

# Clean Docker containers and images
clean_docker:
	@echo "Cleaning up Docker containers and images..."
	# Remove all stopped containers
	docker container prune -f
	# Remove all unused images
	docker image prune -a -f
	# Optional: If you want to remove all containers, whether running or stopped
	# docker rm -f $(docker ps -aq)
	# Optional: If you want to remove all images
	# docker rmi -f $(docker images -aq)
	@echo "Docker cleanup complete."

# Display available commands and usage
help:
	@echo "Available Commands:"
	@echo "  install-dev-tools    Install required development tools"
	@echo "  install-python       Download and install Python $(PYTHON_VERSION)"
	@echo "  install-dependencies Install Python dependencies"
	@echo "  run-streamlit-only   Run only the Streamlit app"
	@echo "  run-fastapi-only     Run only the FastAPI app"
	@echo "  run-all              Start both FastAPI and Streamlit concurrently"
	@echo "  stop                 Stop running services"
	@echo "  clean                Remove installation files and virtual environment"
	@echo "  clean_docker         Remove all Docker containers and images"
	@echo "  docker-compose-up    Build and run Docker Compose"
	@echo "  docker-compose-down  Stop and remove Docker Compose containers"
	@echo "  help                 Show this help message"
