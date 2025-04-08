import re
import json

def CleanOutput(stdout: str, openAI: bool, debug: bool = False):
    
    rawOutput = stdout.choices[0].message.content.strip()

    clean_output = re.sub(r"^```(?:json)?\n|\n```$", "", rawOutput)

    data = json.loads(clean_output)

    try:
        if openAI:
            data = json.loads(stdout.choices[0].message.content.strip())
        elif not openAI:
            data = json.loads(stdout.strip())
        else:
            data = "This should never happen..."
        
        if debug:
            print(f"[DEBUG] openAI: {openAI}")
            print(f"[DEBUG] data: {data}")
        
        return data
        
    except json.JSONDecodeError as e:
        if debug:
            print(f"[ERROR] Failed to decode JSON: {e}")
        return None