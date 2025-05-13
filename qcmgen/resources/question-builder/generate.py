#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "qcmgen>=0.1.0",
# ]
# [[tool.uv.index]]
# name = "local_pypi"
# url = "/home/san/code/local_pypi"
# format = "flat"
# ///
from qcmgen.amcq import QuestionGroup,QuSingleChoice,QuMultipleChoice,QuOpen,QuestionsFile
from qcmgen import script_runner
from random import randint

# nb de questions aléotoires à générer par groupe de question
QUESTION_INSTANCES_NB=3


# 3 exemples de définition des questions dnas les 3 fonctions suivantes (à remplacer):
def question_ouverte(nb=None):
    """exemple de question ouverte attendant une écriture de code
    """
   
    nb=nb or QUESTION_INSTANCES_NB
    qg=QuestionGroup(1,"note-superman")
    data=[('Toto', 20), ('John', 12), ('Johnny', 2), ('Superman', 16)]
    for qu_number in range(nb):
        d=[data[(i+qu_number+1)%4] for i in range(len(data))]
        q=QuOpen(
            question_text=f"On définit : \n\nnotes = {str(d)} \n\nEcrivez l'expression donnant la note de Superman (utilisez la feuille de réponses)",lines=1)
        qg.add_question(q)
    return qg

def question_simple(nb=None):
    """exemple de question simple
    """

    nb=nb or QUESTION_INSTANCES_NB
    qg=QuestionGroup(points=2,group_name="exemple_simple")
    for _ in range(nb):
        alea_1=randint(2,9)
        alea_2=randint(2,9)
        q=QuSingleChoice(
            question_text=f"combien font {alea_1}+{alea_2} ?",
            cols=3)
        q.add_choice(alea_1+alea_2,True)
        q.add_choice(alea_1+alea_2-1,False)
        q.add_choice(alea_1+alea_2+1,False)
        q.add_choice(alea_1+alea_2-2,False)
        q.add_choice(alea_1+alea_2+2,False)
        qg.add_question(q)
    return qg

def question_multiple(nb=None):
    """exemple de question multiple
    """

    nb=nb or QUESTION_INSTANCES_NB
    qg=QuestionGroup(points=3,group_name="exemple_multiple")
    for _ in range(nb):
        alea_1=randint(1,15)
        alea_2=randint(1,alea_1)
        q=QuMultipleChoice(
            question_text=f"Quelle opération donne {alea_1} ?",
            cols=2)
        q.add_choice(f"{alea_1+alea_2}-{alea_2}",True)
        q.add_choice(f"{alea_2}+{alea_1-alea_2}",True)
        q.add_choice(f"{alea_1+alea_2+5}-{alea_1}",False)
        q.add_choice(f"{alea_2+3}+{alea_1-alea_2}",False)
        q.add_choice(f"{alea_2+1}+{alea_1-alea_2}",False)
        qg.add_question(q)
    return qg







def process_questions(amc_project_folder,latex_question_filename):
    qf=QuestionsFile(amc_project_folder,latex_question_filename)


    # Ajouter ici l'appel aux questions
    qf.add_questiongroup(question_ouverte())
    qf.add_questiongroup(question_simple())
    qf.add_questiongroup(question_multiple())
    # fin de l'ajout des question

    qf.flush()

# def main():
#     script_runner.run(process_questions)
    
if __name__ == '__main__':
    script_runner.run(process_questions)
