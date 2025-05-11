from typing import Annotated
from typing_extensions import TypedDict
import os
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("❌ GOOGLE_API_KEY not found in .env")

# State structure
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Tool: Run command
@tool()
def run_command(cmd: str) -> str:
    """
    Takes the command line prompt and executes it on the user's machine and return the output of the command.
    
    Example: run_command(cmd="dir") where dir is command to list the files.
    """
    try:
        result = os.popen(cmd).read()
        return result if result else "✅ Command executed, but no output returned."
    except Exception as e:
        return f"❌ Command execution failed: {e}"

# Tool: Write file
@tool
def write_file(file_path: str, content: str) -> str:
    """
    Writes content to the given file path.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return f"✅ File written successfully: {file_path}"
    except Exception as e:
        return f"❌ File write failed: {e}"

# Initialize LLM
try:
    llm = init_chat_model(
        model_provider="google_genai",
        model="gemini-1.5-flash"
    )
    llm_with_tool = llm.bind_tools(tools=[run_command, write_file])
except Exception as e:
    raise RuntimeError(f"❌ Failed to initialize or bind tools to chat model: {e}")

# Core Chatbot function
def Chatbot(state: State):
    try:
        system_prompt = SystemMessage(content="""
            You are an helpful AI coding assistant who takes input as input from user and based on the available tools you choose the correct tool and execute the commands.

        You can even execute commands and help user with the output of the command.

        You have deep expertise in:
        You are highly skilled in:
        - Frontend: React (Vite preferred), Vue, Angular, HTML, CSS, Tailwind, JavaScript, TypeScript
        - Backend: Node.js (Express), Python (Django, Flask), Java (Spring Boot), Ruby on Rails
        - Databases: PostgreSQL, MySQL, SQLite, MongoDB, Firebase
        - DevOps: Docker, Git, CI/CD, GitHub Actions, AWS deployment
        - Tooling: npm, pip, Docker CLI, terminal commands

        TOOLING INSTRUCTION
        You can interact with the environment via the following tools:
        
        `run_command(command: str)`  
            - Executes a shell command (string input only).
            - Do NOT pass dictionaries or malformed commands.
            - Windows OS assumed — use correct syntax accordingly.

        `write_file(file_path: str, content: str)`  
            - Writes the given content to the specified path.
            - Ensure that content is complete and context-aware.


        call the relavant tools
                                      
        Note: Make sure to always create the file in the current directory.
        """)
        message = llm_with_tool.invoke([system_prompt] + state["messages"])
        assert len(message.tool_calls) <= 1
        return {"messages": [message]}
    except Exception as e:
        return {"messages": [{"role": "system", "content": f"❌ Error during chat logic: {e}"}]}

# LangGraph construction
try:
    tool_node = ToolNode(tools=[run_command, write_file])
    graph_builder = StateGraph(State)

    graph_builder.add_node("Chatbot", Chatbot)
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_edge(START, 'Chatbot')
    graph_builder.add_conditional_edges("Chatbot", tools_condition)
    graph_builder.add_edge('tools', "Chatbot")
    graph_builder.add_edge('Chatbot', END)

    graph = graph_builder.compile()
except Exception as e:
    raise RuntimeError(f"❌ Failed to build LangGraph: {e}")

# Factory method with error handling
def create_chat_graph(checkpointer=None):
    try:
        return graph_builder.compile(checkpointer=checkpointer)
    except Exception as e:
        print(f"❌ Error compiling chat graph with checkpointer: {e}")
        return None
