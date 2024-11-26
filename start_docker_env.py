import os

from pyreact_agent.docker_env.utils import build_docker_image, run_docker_image, start_container_by_name


if __name__ == "__main__":
    # Variables for building docker image
    build_image = True
    docker_url = None
    image_name = 'my-python-env'
    dockerfile_path = './pyreact_agent/docker_env'

    # Variables for running docker image as new container
    run_container = True
    container_name = 'pyreact-agent-container'
    local_bound_dir = None

    # Variables for starting docker container
    start_container = True

    # Build docker image
    if build_image:
        build_docker_image(
            dockerfile_path=dockerfile_path,
            image_name=image_name,
            docker_url=docker_url
        )

    # Run docker container
    if run_container:
        if local_bound_dir is None:
            local_bound_dir = os.getcwd()

        run_docker_image(
            image_name=image_name,
            local_bound_dir=local_bound_dir,
            container_name=container_name,
            docker_url=docker_url
        )

    # Start container
    if start_container or run_container:
        start_container_by_name(
            container_name=container_name,
            docker_url=docker_url
        )
