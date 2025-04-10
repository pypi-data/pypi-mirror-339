# Variables
IMAGE_NAME = elementfm/mcp
CONTAINER_NAME = mcp
PORT = 8000

# Default target
.PHONY: all
all: build run

# Build the Docker image
.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
.PHONY: run
run:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):$(PORT) $(IMAGE_NAME)

# Stop and remove the Docker container
.PHONY: stop
stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

# Remove the Docker image
.PHONY: clean
clean: stop
	docker rmi $(IMAGE_NAME)

# View Docker container logs
.PHONY: logs
logs:
	docker logs -f $(CONTAINER_NAME)
