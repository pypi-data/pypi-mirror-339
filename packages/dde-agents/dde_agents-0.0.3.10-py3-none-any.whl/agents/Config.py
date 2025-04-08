class ModelConfig:
    _model = None
    _openai = None

    @classmethod
    def setDefaultModel(cls, model: str, openAI: bool):
        cls._model = model
        cls._openai = openAI

    @classmethod
    def getDefaultModel(cls):
        return cls._model

    @classmethod
    def getDefaultOpenAI(cls):
        return cls._openai
