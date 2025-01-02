#!/usr/bin/env bash
set -o errexit
set -o nounset

IMAGE_NAME="ondo"
CONTAINER_NAME="ondo-server"
CONTAINER_RUNTIME="docker"

# if podman, use podman instead of docker
# if command -v podman &>/dev/null; then
# 	CONTAINER_RUNTIME="podman"
# fi

function run {
	echo "Building image"
	ensure-image
	echo "Starting container"
	start-container
}

function build {
	ensure-image
}

function ensure-image {
	docker build -t ${IMAGE_NAME} .
}

function start-container {
	# if ${CONTAINER_RUNTIME} ps -a | grep ${IMAGE_NAME} &>/dev/null; then
	# 	echo "Container already exists"
	# 	return
	# fi
	${CONTAINER_RUNTIME} run \
		--name ${CONTAINER_NAME} \
		--publish 8000:8000 \
		--env-file .env.docker \
		--volume ${PWD}/data:/data \
		${IMAGE_NAME}
		# --detach \
}

function clean {
	${CONTAINER_RUNTIME} stop ${CONTAINER_NAME} || true
	${CONTAINER_RUNTIME} rm -fv ${CONTAINER_NAME} || true
}

"$@"
