from Agent import Agent
from Chain import Chain
from Config import ModelConfig

ModelConfig.setDefaultModel("gpt-4o", True)

john = Agent(
    name="john",
    instruction="You are john, you need to figure out a solution based on the problem.",
)

sam = Agent(
    name="sam",
    instruction="You are sam, you need to figure out a solution based on the problem.",
)

if __name__ == "__main__":
    chain = Chain([john, sam])
    chain.runUntil("whats the best way to save engergy?", "consensus reached", debug=True)
