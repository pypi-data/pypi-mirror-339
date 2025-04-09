import logging
from langchain_ollama import ChatOllama




def load_model(name="mistral:7b-instruct-v0.3-fp16", base_url="http://localhost:21434", temperature:float=0,**kwargs) ->ChatOllama :
    """
    Créé et retourn un modèle ChatOllaman
    """
    try :
        model = ChatOllama( model=name,
                    base_url=base_url,
                    temperature=temperature,
                    client_kwargs=kwargs )
        return model
    except Exception as ex :
        logging.critical(f"Exception pendant le chargement du modèle {name} avec l'exeception : \n{ex}")
        return None 