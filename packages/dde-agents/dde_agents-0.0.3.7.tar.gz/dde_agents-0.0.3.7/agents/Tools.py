import inspect
import re
import json
import functools

from functools import wraps

from Agent import Agent

defaultModel = "gpt-4o"
defaultOpenAI = True

debug = False

def dynamicTool(function):
    @functools.wraps(function)
    def wrapper(*args, prompt=None, **kwargs):
        sig = inspect.signature(function)

        try:
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            return function(*args, **kwargs)
        
        except TypeError as e:
            if debug:
                print(f"[DEBUG] Argument mismatch, AI gaat invullen: {e}")

        source = inspect.getsource(function)
        param_list = list(sig.parameters.keys())

        dynamicAgent = Agent(
            name="dynamicAgent",
            instruction="",
            model=defaultModel,
            openAI=defaultOpenAI,
            outputGuardrails="You need to check if the given parameters will not cause problems, so dont't use spaces in links. Or other erros that can be prevented."
        )

        prompt_for_params = f"""
            You are now an AI agent.

            Agent information:
                - Agent name: {dynamicAgent.name}
                - Agent instruction: {dynamicAgent.instruction}
                - Function parameters: {param_list}
                - Function code: {source}
                - User prompt: {prompt}

            The above list defines you. You can't make any other info up.

            You need to generate the right parameters for the function. So the right output will be given. If the name is somehting like city then don't give a country as parameter. And other stuff like that.

            Respond ONLY with valid JSON like:

            {{
                "parameters": {{
                    "parameter1": "value1",
                    "parameter2": "value2"
                }}
            }}
        """

        stdout = dynamicAgent.runOpenAI(prompt_for_params, debug=debug)
        rawOutput = stdout.choices[0].message.content.strip()

        clean_output = re.sub(r"^```(?:json)?\n|\n```$", "", rawOutput)

        try:
            data = json.loads(clean_output)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to parse JSON: {e}")
            return None

        if "parameters" not in data:
            print("[ERROR] JSON is missing 'parameters' key.")
            return None

        return function(**data["parameters"])

    wrapper.__dynamic_tool__ = True # Add for the toolcheck thingy 
    return wrapper



@dynamicTool
def _getWeatherData(city: str):
    if city.lower() == "london":
        return "London: sun"
    elif city.lower() == "singapore":
        return "Singapore: amazing weather"
    elif city.lower() == "washington dc":
        return "Washington DC: thunder"
    else:
        return f"{city}: no weather data found."

agent = Agent(
    name="agent",
    instruction="You need to run the tools based on the prompt",
    model="gpt-4o",
    openAI=True,
    tools=[_getWeatherData]
)


if __name__ == "__main__":
    r = agent.run(input("prompt: "), debug=debug, disableGuardrails=False)
    print(r)