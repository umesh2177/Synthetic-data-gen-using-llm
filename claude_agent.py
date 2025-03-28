from phi.agent import Agent, RunResponse
from phi.model.anthropic import Claude

agent = Agent(
    model=Claude(id="cclaude-3-5-sonnet-20240620",api_key="uAhFmvjgRI8sK2kmwwAA"),
    markdown=True
)

# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story.")
# print(run.content)

# Print the response on the terminal
agent.print_response("Share a 2 sentence horror story.")

##fail due to api key