import json
from typing import Dict, Any, List, Tuple, Optional
#from langchain_community.llms import Ollama
# Import OllamaLM from langchain_ollama
from langchain_ollama import OllamaLLM as Ollama
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from pydantic import BaseModel, Field
from mainframe_demo.tools.story_generator import StoryGeneratorTool
from mainframe_demo.config.settings import settings
from mainframe_demo.tools.user_story_generator import UserStoryAPITool

class AgentState(BaseModel):
    """Represents the current state of the agent"""
    input: str = Field(description="The input business rule")
    current_step: str = Field(description="Current step in the process")
    generated_story: Optional[Dict] = Field(default=None, description="Generated user story")
    user_stories: Optional[Dict] = Field(default=None, description="Generated user stories from API")
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")
    completed: bool = Field(default=False, description="Whether the process is complete")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

def create_story_graph() -> StateGraph:
    """Creates the state graph for story generation"""
    print("Within the create_story_graph method ::::: ")
    
    # Initialize tools
    tools = [StoryGeneratorTool(), UserStoryAPITool()]
    tool_executor = ToolExecutor(tools)
    
    # Initialize LLM
    llm = Ollama(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.MODEL_NAME
    )

    # Add new function to generate user stories
    def generate_user_stories(state: AgentState) -> AgentState:
        """Generates user stories using the API"""
        print("Within generate_user_stories method")
        try:
            print(f"before the tool_executor.invoke method ::::")
            tool_invocation = ToolInvocation(
                tool="user_story_api",
                tool_input=state.input
            )
            
            result = tool_executor.invoke(tool_invocation)

            story_data = {
                "generated_story": state.input,  # Your generated story value
                "user_stories": result.get('data')       # Your user stories value
            }
            
            state.input = story_data
            state.current_step = "user_stories_generated"
            state.completed = True
            return state
        except Exception as e:
            print(f"Error in API call:")
            state.errors.append(f"User stories generation error: {str(e)}")
            state.completed = True
            return state    

    # Define the generation step
    def generate_story(state: AgentState) -> AgentState:
        """Generates the user story using the tool"""
        print("Within the generate_story method")
        try:
            print("before the tool_executor.invoke method :::: ")
            # Create tool invocation
            tool_invocation = ToolInvocation(
                tool="story_generator",
                tool_input=state.input
            )
            
            result = tool_executor.invoke(tool_invocation)
            print(f"after the tool_executor.invoke method ::::")
            
            state.input = result.get('data')
            state.current_step = "generation_completed"
            print("after the tool_executor.invoke method :::: ")
            return state
        except Exception as e:
            print(f"Error in tool execution:")
            state.errors.append(f"Generation error: {str(e)}")
            state.completed = True
            return state


    # Define the router
    def router(state: AgentState) -> str:
        """Routes to the next step based on current state"""
        if state.errors:
            return END
        if state.completed:
            return END
        if state.current_step == "":
            return "generate"
        if state.current_step == "generation_completed":
            return "generate_user_stories"
        if state.current_step == "user_stories_generated":
             return END
        return END

    # Create the workflow
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("generate", generate_story)
    workflow.add_node("generate_user_stories", generate_user_stories)
       
    # Add edges
    workflow.add_edge("generate", "generate_user_stories")
    workflow.add_edge("generate_user_stories", END)
    
    # Set entry point
    workflow.set_entry_point("generate")
    print("after the workflow method ::::: ")
    
    return workflow

def process_business_rule(business_rule: str) -> Dict[str, Any]:
    """
    Process a business rule and generate a user story.
    
    Args:
        business_rule: The mainframe business rule
        
    Returns:
        Dict containing the generated story and process metadata
    """
    try:
        # Create initial state
        initial_state = AgentState(
            input=business_rule,
            current_step="",
            metadata={},
            errors=[],
            completed=False
        )
        print("Initial state created")
        print(initial_state.current_step)
        
        # Create and run the graph
        graph = create_story_graph()
        print("Graph created")
        app = graph.compile(
            #debug=True
        )
        print("Graph compiled")
        result = app.invoke(initial_state)
        
        print("Graph invoked")

        # if result.errors:
        #     return {
        #         "status": "error",
        #         "errors": result.errors
        #     }
        
        
        return {
            "status": "success",
            "result": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }