# PyReact-Agent

PyReact-Agent is a Python package that provides tools for creating an LLM ReAct agent. 

This package also includes tools that an LLM can use for running Bash or Python code inside Docker containers with enhanced control and flexibility. It is designed to be simple to use, making it easy to set up Docker environments and execute Python scripts, even from within a Jupyter Notebook.

## Features

- **Create LLM ReAct Agents Easily**: Create a ReAct agent with tools in just a few lines of code.
- **Framework for creating custom LLM Tools**: Use the ToolSet classes to create custom toolsets, or turn any simple python function into a tool that an LLM can use
- **Build Docker Images**: Build Docker images from a `Dockerfile` with a single function call.
- **Manage Containers**: Start, stop, and fetch existing Docker containers programmatically.
- **Run Python Code in Docker**: Start and interact with Python Docker containers seamlessly.

## Roadmap

- **Integration with Open WebUI using Pipelines**: Use Open WebUI's Pipelines to use ReAct agents from this package with the Open WebUI frontend framework
- **Integration with 3rd Party LLM Providers**: Use this package with LLM providers. Currently only Ollama is supported.
- **RAG Integration**: A simple in-package RAG system + integration with other 3rd party rag providers
- **Memory Management**: Ability to self-manage memory for a single query, so that queries with multiple steps can be managed more gracefully.

## Installation

To install PyReact-Agent, run:

```bash
pip install pyreact_agent
```

## Usage

### End-To-End

See example.py for a full end-to-end working example of how to create and run a ReAct agent with code writing tools.

### Building a Docker Image

To build a Docker image using the `Dockerfile` in your project:

```python
from pyreact_agent import docker_utils

docker_utils.build_docker_image(image_name="my-python-env")
```

### Starting a Python Docker Environment

To start a Docker container and run Python code inside:

```python
docker_utils.run_docker_image(
    image_name="my-python-env",
    container_name="my-python-container",
    local_bound_dir="/path/to/your/local/dir"
)
```

### Managing Containers

#### Start a Stopped Container

```python
docker_utils.start_container_by_name("my-python-container")
```

#### Stop a Running Container

```python
docker_utils.stop_container_by_name("my-python-container")
```

#### Get an Existing Container

```python
container = docker_utils.get_container("my-python-container")
```

#### Get a Docker Image

```python
image = docker_utils.get_image("my-python-env")
```

## Requirements

- Python 3.9 or higher
- Docker installed and running
- Ollama server (if running LLM locally)

## Contributing

Contributions are welcome! If you have ideas, suggestions, or bug reports, please feel free to submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Author

Cody Maughan
[GitHub Profile](https://github.com/CodyAMaughan)

## Acknowledgments

- Thanks to the Python and Docker communities for their incredible support and tools.

---

Happy coding with PyReact-Agent!
