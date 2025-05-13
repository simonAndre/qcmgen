import sys
from pathlib import Path

def get_help():
    print(f"""
randomized questions builder formated for AMC

Usage: {sys.argv[0]} [AMC_project_dir] [questiongroup.tex]
    with:
    - [AMC_project_dir]: AMC project directory
    - [questiongroup.tex]: latex file for the AMC question group to generate
        """)

def throw_error(errmsg):
    print("---------------------")
    print(f"ERROR: {errmsg}")
    print("---------------------")
    get_help()
    exit(1)

def run(questionlist_func):
    """Lance la génération des questions aléatoires spécifiques

    Args:
        questionlist_func (function): fonction prenant 2 arguments: 
            - le repertoire du projet AMC cible 
            - le nom du fichier de question à générer au format latex 
    """
    if len(sys.argv)!=3:
        throw_error("mauvais arguments")
    if not Path(sys.argv[1]).exists():
        get_help()
        throw_error(f"le repertoire {sys.argv[1]} n'existe pas.")

    qfname="randomized_question_groups.tex"
    if len(sys.argv)>1:
        qfname=sys.argv[2]

    questionlist_func(sys.argv[1],qfname)

if __name__=="__main__":
    run()