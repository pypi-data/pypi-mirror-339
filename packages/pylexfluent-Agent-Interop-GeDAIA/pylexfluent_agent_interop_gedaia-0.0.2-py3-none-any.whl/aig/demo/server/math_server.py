# math_server.py
from mcp import GetPromptResult, Resource
from mcp.types import Prompt, PromptArgument, PromptMessage, TextContent
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Settings
import asyncio 

settings:Settings=Settings(port=8000,log_level="DEBUG")
mcp = FastMCP("Math",settings=settings)

@mcp.tool()
def Ajouter(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

@mcp.tool()
def Multiplier(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def diviser(a: float, b: float) -> float:
    """Divide two numbers"""
    if b!=0 :
        return a / b
    else :return None

@mcp.resource("files://{file_id}/object_ref")
def get_file_profile(file_id: str) -> str:
    """Dynamic file data"""
    return f"gedaia/mcp/{file_id}/file"


@mcp._mcp_server.list_resources()
async def handle_list_resources()-> list[Resource] :
    return [
        Resource(
            uri="files://{file_id}/object_ref",
            name="Fichier dans le stockage interne",
            description="Récupérer le lien du file_id dans le stockage interne"
        )
    ]

  
PROMPT_CALCULATOR="Calculator-prompt"  
DESCRIPTION_CALCULATOR_PROMPT="prompt pour calculer des opération d'addition, multiplication et division entre deux termes"

@mcp._mcp_server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> GetPromptResult:
    if name != PROMPT_CALCULATOR:
        raise ValueError(f"Unknown prompt: {name}")

    return GetPromptResult(
        description=DESCRIPTION_CALCULATOR_PROMPT,
        messages=[
            PromptMessage(
                role="user",
                arguments=arguments,
                content=TextContent(type="text", 
    text=f"""
    Vous êtes un agent intelligent capable de répondre aux questions et d'effectuer des tâches et utilisant exlusivement les outils mis à ta disposition.
    Calcule l'opération ci-dessous:\n{arguments['operation']} 
    """
                ),
            )
        ],
    )
    

    
@mcp._mcp_server.list_prompts()
async def handle_list_prompts() ->list[Prompt] :
    return [
        Prompt(
            name=PROMPT_CALCULATOR,
            description=DESCRIPTION_CALCULATOR_PROMPT,
            arguments=[
                PromptArgument(
                    name="operation", description ="expression de l'opération"
                ),
            ]
        )
        
    ]

def start_demo_server(port:int=8000) :
    """
    Démarre le serveur démo 
    """
    mcp.settings.port=port
    asyncio.run(mcp.run(transport="sse"))    

if __name__ == "__main__":
    start_demo_server(port=8005)