import json
import subprocess

from agents.Agent import Agent
from agents.Config import ModelConfig
from agents.CleanOutput import CleanOutput

def terminalUse(task: str, debug: bool = False) -> str:
    _taskAgent = Agent(
        name="_agent",
        instruction="You need to break the task in steps that can be done in 1 command.",
    )
    _commandAgent = Agent(
        name="commandAgent",
        instruction="From the given steps you need to give me commands",
    )

    promptTaskAgent = f"""
        "You are now an AI agent.

        Agent information:
            - Agent name: {_taskAgent.name}
            - Agent instruction: {_taskAgent.instruction}
            - Task: {task}

        The above list defines you. You can't make any other info up.
        
        You to break down the task into steps that can be done in 1 command.
            
        Follow these instructions precisely."
    """
    
    response = _taskAgent.run(prompt=promptTaskAgent, debug=debug)

    promptCommandAgent = f"""
        "You are now an AI agent.

        Agent information:
            - Agent name: {_commandAgent.name}
            - Agent instruction: {_commandAgent.instruction}
            - Steps: {response}

        The above list defines you. You can't make any other info up.
        
        You need to give commands to fulfill the steps.
        
        You need to give an output like this (valid JSON):

        {{
            "commands": [
                {{
                    "id": "1",
                    "command": "{{enter command here}}"
                }},
                {{
                    "id": "2",
                    "command": "{{enter command here}}"
                }}
            ]
        }}

        Extra instructions:
            - You need to only generate command for the given steps. So don't add unnecessary steps. 
            - Only Respond with valid json. Don't add anything else so no: '```json'
            
        Follow these instructions precisely."
    """
    
    taskResponse = _commandAgent.run(prompt=promptCommandAgent, debug=debug)
    taskResponse = CleanOutput(stdout=taskResponse, openAI=ModelConfig.getDefaultOpenAI(), debug=debug)

    try:
        commandsJson = json.loads(taskResponse)
        for cmd in commandsJson.get("commands", []):
            print(f"\nRunning command [{cmd['id']}]: {cmd['command']}")
            result = subprocess.run(cmd["command"], shell=True, capture_output=True, text=True)
            print(f"Output:\n{result.stdout}")
            if result.stderr:
                print(f"Errors:\n{result.stderr}")
    except json.JSONDecodeError:
        print("Failed to parse command output as JSON")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    ModelConfig.setDefaultModel("gpt-4o", True)
    terminalUse("Scan netwerk op actieve hosts", debug=True)
