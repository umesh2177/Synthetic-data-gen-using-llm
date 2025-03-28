from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
load_dotenv()
import os
#

def sd_json_agent(question,sample_data,metadata,api_key_input="",model="llama3-70b-8192"):
    web_agent = Agent(
        # model=Groq(id=model,api_key=os.getenv("Groq_api_key")),
        model=Groq(id=model,api_key=api_key_input),
        description="""This agent generates synthetic data.""",
        # description=description,
        add_chat_history_to_messages=True,
        # tools=[DuckDuckGo(fixed_max_results=10)],
        instructions=[
            f"""You have to provide the synthetic data in json for the given metadata  {metadata}.
                Generate {10} records for this metadata.
                for example: real data is  {sample_data}.""",
                "Don't add any others lines , Provide only data output.",
                

        ],
        show_tool_calls=True,
        markdown=True,
    )
    # response = web_agent.print_response(question, stream=False)
    response=web_agent.run(question, stream=False).to_dict()
    print(f"{response.keys()=}")
    print(response["messages"][-1]["content"])
    return response["messages"][-1]["content"]

