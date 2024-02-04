from internal.US3_sacherverhalt import load_document

from langchain.prompts.pipeline import PipelinePromptTemplate
from langchain.prompts.prompt import PromptTemplate



def bescheidTemplate(sachverhalt:str,prüfungsergebnis) -> PipelinePromptTemplate:   
    regeln = load_document("./input_docs/regeln.docx")
    beispiel_bescheid = load_document("./input_docs/Bescheid1.docx")
    
    full_template = PromptTemplate.from_template(
        """"
        Du bist ein nützlicher Assistent für Mitarbeiter der Stadtverwaltung und hilfst dabei,einen Bescheid zu verfassen.
        Die Erstellung eines Bescheides erfolgt in folgenden Schritten:
        1.Den gegebenen Sachverhalt analysieren, um zu verstehen, was passiert ist und was berücksichtigt werden soll.
            Hier ist der zu analysierende und verarbeitende Sachverhalt:
            {sachverhalt}
        2.Den Beispielbescheid und das Muster eines Beispielbescheids analysieren, um Erkenntnisse zu gewinnen.
            Aus einem Sachverhalt wird der folgende Beispiel_Bescheid generiert: {bsl_bescheid}
        3.Unter Berücksichtigung der Sachverhaltsprüfung einen sachlichen und ausführlichen Bescheid verfassen.
        Sachverhaltsprüfung : {sachverhaltsprüfung}
        Format: 
            Der zu erstellende Bescheid umfasst fünf Abschnitte:
            1. Einleitung 
            2. Tenor (Entscheidungsformel)
            3. Begründung
            4. Rechtsbehelfsbelehrung
            5. Unterschrift mit Grußformel
        Bescheid:
        """
        )
    message = full_template.format(
        sachverhalt= sachverhalt,
        bsl_bescheid= beispiel_bescheid,
        sachverhaltsprüfung= prüfungsergebnis
        )
    return message

    