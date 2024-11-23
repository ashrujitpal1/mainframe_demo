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

class AgentState(BaseModel):
    """Represents the current state of the agent"""
    input: str = Field(description="The input business rule")
    current_step: str = Field(description="Current step in the process")
    generated_story: Optional[Dict] = Field(default=None, description="Generated user story")
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")
    completed: bool = Field(default=False, description="Whether the process is complete")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

def create_story_graph() -> StateGraph:
    """Creates the state graph for story generation"""
    print("Within the create_story_graph method ::::: ")
    
    # Initialize tools
    tools = [StoryGeneratorTool()]
    tool_executor = ToolExecutor(tools)
    
    # Initialize LLM
    llm = Ollama(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.MODEL_NAME
    )

    # # Define the analysis step
    # analysis_prompt = ChatPromptTemplate.from_messages([
    #     ("system", """You are a Scrum Master expert in generating user story.
    #      From the user input, identify if the input is to create the user stories. 
    #      You use the Tool: StoryGeneratorTool to generate the user stories"""),
    #     ("user", "{input}")
    # ])
    # print("after the analysis_prompt method ::::: ")

    # def analyze_input(state: AgentState) -> AgentState:
    #     """Analyzes the input business rule"""
    #     try:
    #         print("Within the analyze_input method")
    #         prompt = analysis_prompt.format_messages(input=state.input)
    #         print(prompt)
    #         analysis = llm.invoke(prompt)
    #         state.current_step = "analysis_completed"
    #         return state
    #     except Exception as e:
    #         state.errors.append(f"Analysis error: {str(e)}")
    #         state.completed = True
    #         return state

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
            
            state.generated_story = result
            state.current_step = "generation_completed"
            print("after the tool_executor.invoke method :::: ")
            return state
        except Exception as e:
            print(f"Error in tool execution:")
            state.errors.append(f"Generation error: {str(e)}")
            state.completed = True
            return state

    # # Define the review step
    # review_prompt = ChatPromptTemplate.from_messages([
    #     ("system", """Review the generated user story. Ensure it:
    #     1. Follows proper user story format
    #     2. Captures all requirements
    #     3. Includes acceptance criteria
    #     4. Is clear and actionable"""),
    #     ("user", "{story}")
    # ])

    # def review_story(state: AgentState) -> AgentState:
    #     """Reviews and enhances the generated story"""
    #     try:
    #         if state.generated_story:
    #             review = llm.invoke(review_prompt.format_messages(
    #                 story=str(state.generated_story)
    #             ))
    #             state.generated_story["review"] = review
    #         state.current_step = "review_completed"
    #         state.completed = True
    #         return state
    #     except Exception as e:
    #         state.errors.append(f"Review error: {str(e)}")
    #         state.completed = True
    #         return state

    # Define the router
    def router(state: AgentState) -> str:
        """Routes to the next step based on current state"""
        if state.errors:
            return END
        if state.completed:
            return END
        if state.current_step == "":
            return "generate"
        # if state.current_step == "analysis_completed":
        #     return "generate"
        if state.current_step == "generation_completed":
             return END
        return END

    # Create the workflow
    workflow = StateGraph(AgentState)
    
    # Add nodes
    #workflow.add_node("analyze", analyze_input)
    workflow.add_node("generate", generate_story)
    #workflow.add_node("review", review_story)
    
    # Add edges
    #workflow.add_edge("analyze", "generate")
    # workflow.add_edge("generate", "review")
    # workflow.add_edge("review", END)
    workflow.add_edge("generate", END)
    
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
        print(f"app.invoke result: {result}")
        
        print("Graph invoked")
        # Process result
        # if result.errors:
        #     return {
        #         "status": "error",
        #         "errors": result.errors
        #     }
        
        
        return {
            "status": "success",
            "story": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }