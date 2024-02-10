
from langchain.prompts.prompt import PromptTemplate
def interaktion_prompt(sachverhalt, original_text, user_query):
    prompt_template = PromptTemplate.from_template(
        """ Du bist Sachbearbeiter und Verfasser eines juristischen Bescheids.
            Anhand einen Sachverhalt wird ein originaler Bescheid wie folgendes generiert. 
            sachverhalt : {sac}
            originaler Bescheid : {original}
            Auf Basis von Fragen oder Kommentare von den Benutzer solltest du diesen Bescheid erneut verfassen.
            Änderungswünsche vom Benutzer : {query}
            Der neue Text : 
        """ 
    )
    messages = prompt_template.format(
        sac = sachverhalt,
        original = original_text,
        query = user_query
        )
    return messages