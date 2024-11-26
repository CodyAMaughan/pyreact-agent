from pyreact_agent.tools.core import Tools
from pyreact_agent.tools.custom import get_now
from pyreact_agent.tools.docker_env import PythonDockerToolSet
from pyreact_agent.clients.ollama import OllamaClient
from pyreact_agent.agent import ReActAgent
from pyreact_agent.docker_env.utils import run_docker_image, build_docker_image


# Main program
if __name__ == "__main__":
    # Build docker image (if it doesn't already exist, will throw an error if it already exists
    build_docker_image(image_name='my-python-env')

    # Start docker container environment (if it doesn't already exist, otherwise will throw an error)
    run_docker_image(image_name='my-python-env',
                     container_name='my-python-container')

    # Create tools object
    available_tools = [get_now]
    available_tool_sets = [PythonDockerToolSet(container_name='my-python-container')]
    tools = Tools(tool_list=available_tools, tool_sets=available_tool_sets)

    # Instantiate the LLM client and agent
    llm_client = OllamaClient(
        base_url="http://localhost:11434",  # Change your base-url here if needed\
        model='llama3'  # Change your model here if needed
    )

    # Create the ReAct Agent
    agent = ReActAgent(llm_client, tools)

    # Ask a question
    question = ("What is the current date and time? "
                "Please write the answer to a file named 'time.txt'.")

    print('=====================')
    print('START MESSAGES')
    print('=====================')
    print(f'user: {question}')
    print('=====================')
    for message in agent.reason_and_act(question):
        # This allows you to see the internal thoughts and tool calls,
        #     but really the last message with the Final Answer is what you want.
        print(message)
        print('=====================')
