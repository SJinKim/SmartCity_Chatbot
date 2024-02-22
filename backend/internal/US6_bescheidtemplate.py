#from US3_sacherverhalt import load_document # for Backend-Test
from internal.US3_sacherverhalt import load_document

from langchain.prompts.pipeline import PipelinePromptTemplate
from langchain.prompts.prompt import PromptTemplate



def bescheidTemplate(sachverhalt:str,prüfungsergebnis) -> PipelinePromptTemplate:
    """ Generates an official notice (Bescheid) template based on the provided case file (Sachverhalt) and examination result (Sachverhaltsprüfung).

    Args:
        sachverhalt (str): The case file (Sachverhalt) text.
        prüfungsergebnis (str): The case file examination (Sachverhaltsprüfung) text.

    Returns:
        PipelinePromptTemplate: A template containing instructions and placeholders for generating an official notice (Bescheid).
    """
    beispiel_bescheid = load_document("./input_docs/Bescheid1.docx")
    
    full_template = PromptTemplate.from_template(
        """"
        Du bist ein nützlicher Assistent für juristische Mitarbeiter der Stadtverwaltung und hilfst dabei, einen Bescheid basierend auf einen Sachverhalt zu verfassen.
        Die Erstellung eines Bescheides erfolgt in folgenden Schritten:
        1. Den gegebenen Sachverhalt analysieren, um zu verstehen, was passiert ist und was berücksichtigt werden soll.
            Hier ist der zu analysierende und zu verarbeitende Sachverhalt:
            {sachverhalt}
        2. Den Beispielbescheid und das Muster eines Beispielbescheids analysieren, um Erkenntnisse zu gewinnen.
            Aus einem Sachverhalt wird der folgende Beispiel_Bescheid generiert: {bsl_bescheid}
        3. Unter Berücksichtigung der Sachverhaltsprüfung einen sachlichen und ausführlichen Bescheid verfassen.
        Sachverhaltsprüfung: {sachverhaltsprüfung}
        Format: 
            Das zu erstellende Bescheid umfasst fünf Abschnitte:
            1. Einleitung: Briefkopf, Betreff (schlagwortartige Andeutung des Bescheids), Anrede und Überleitungssatz zum Tenor
            2. Tenor (Entscheidungsformel): rechtliche Maßnahmen für Pflichtigen
            3. Begründung: tatsächliche Gründe und rechtliche Gründe mit Ermessenserwägungen
            4. Rechtsbehelfsbelehrung: Rechtsbehelf (z.B. Widerspruch, Anfechtungsklage, Berufung, Revision) muss namentlich die Behörde, bei der er einzulegen ist, deren Sitz und die einzuhaltende Frist angeben
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

    