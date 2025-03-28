from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
load_dotenv()
import os

def python_code_agent(question,sample_data,metadata,api_key_input="",model="llama3-70b-8192"):
    web_agent = Agent(
        # model=Groq(id=model,api_key=os.getenv("Groq_api_key")),
        model=Groq(id=model,api_key=api_key_input),
        description="""This agent generates synthetic data using Groq API.""",
        # description=description,
        add_chat_history_to_messages=True,
        # tools=[DuckDuckGo(fixed_max_results=10)],
        instructions=[
            f"""You have to provide the synthetic data for the given metadata  {metadata}.
                Collumns: {metadata["columns"]} should be same generete 100 records for this metadata.
                for example: {sample_data}.
            """,
            """You can use the following libraries to generate synthetic data: Faker, NumPy, Pandas, etc.""",
            """You can use the following types of data: int64, float64, object, Date etc.""",
            """You can use the sample data provided to identify the data types.""",
            """You can modify the metadata details if needed.""",

        ],
        show_tool_calls=True,
        markdown=True,
    )
    # response = web_agent.print_response(question, stream=False)
    response=web_agent.run(question, stream=False).to_dict()
    print(f"{response.keys()=}")
    print(response["messages"][-1]["content"])
    return response["messages"][-1]["content"]

