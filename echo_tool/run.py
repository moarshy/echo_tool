from pydantic import BaseModel
from typing import Optional, Dict, Any

class InputSchema(BaseModel):
    func_name: str
    func_args: Optional[dict] = None


import logging
from typing import Dict, List, Union
from echo_tool.schemas import InputSchema
from naptha_sdk.schemas import AgentRunInput

logger = logging.getLogger(__name__)


def run(module_run: Dict, *args, **kwargs) -> Union[List[Dict], Dict]:
    module_run = AgentRunInput(**module_run)
    module_run.inputs = InputSchema(**module_run.inputs)

    logger.info(f"Running function: {module_run.inputs.func_name}")
    logger.info(f"Input: {module_run.inputs}")
    
    if module_run.inputs.func_name == "list_tools":
        return [
            {
                "name": "echo",
                "description": "Echo a message",
                "input_schema": {
                    "type": "object",
                    "required": ["message"],
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Message to echo back",
                        }
                    },
                },
            }
        ]
    elif module_run.inputs.func_name == "call_tool":
        if not module_run.inputs.func_args:
            raise ValueError("func_args is required for call_tool")
            
        tool = module_run.inputs.func_args.get("tool")
        if not tool:
            raise ValueError("tool parameter is required")
            
        if tool == "echo":
            message = module_run.inputs.func_args.get("arguments").get("message")
            if not message:
                raise ValueError("message parameter is required for echo tool")
                
            return {"type": "text", "text": message}
        else:
            raise ValueError(f"Unknown tool: {tool}")
    else:
        raise ValueError(f"Invalid function name: {module_run.inputs.func_name}")