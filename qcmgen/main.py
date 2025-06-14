import click
from pathlib import Path
from .template_mgr import create_project_structure,get_curr_project_dir,renderjinja
from .amc_commands import prepare_project,open_AMC
from .common.utils import import_from_source_file,print_error,BadArgsError, UserError
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
# @click.version_option(version='1.0.0')
@click.version_option()
def main() -> None:
    """
    script de gestion de QCM papiers dynamiques basés sur auto-multiple-choice
    S. ANDRE, 2025    
    """
    pass

@main.command()
@click.argument('folder')
@click.option('--overwrite', is_flag=True, help='écrase le rep projet s''il existe déjà')
@click.option('--answersheet', is_flag=True, help='utilise une feuille de réponse séparée des questions (sinon, les réponses doivent être apportées dans la feuille de questions)')
def init(folder,overwrite,answersheet):
    """
    crée le repertoire AMC à partir de la structure de projet par défaut et 
    des fichiers templates contenus dans le repertoire qcmgen.ressources.amc_bootstrap_template 
    du présent package
    """
    prjectdata={"separatedanswershet":answersheet}
    create_project_structure(folder,overwrite,prjectdata)
    open_AMC(Path(folder))

@main.command()

@click.argument('folder',default=".")
def reapply(folder:str):
    """reapplique la préparation des documents imprimables en fonction des fichiers .tex source.
    Attention : ne pas executer une fois les copies imprimées, toute la géométrie est modifiée."""
    try:
        amcproj=get_curr_project_dir(folder)
        prepare_project(amcproj)
    except UserError as e:
        print_error(e.message)

@main.command()
@click.argument('folder')
def amc(**kwargs):
    """lance l'IHM d'AMC"""
    amcproj=Path(kwargs["folder"])
    if amcproj.exists():
        open_AMC(amcproj)
    else:
        print("ERREUR: le repertoire projet n'existe pas")

# @main.command()
# def testrender(**kwargs):
#     from .common.jinja_templating import renderjinja
#     d={
#         "amcq":{
#             "maxpoints":4,
#             "questionid":"qtest-1",
#             "content":"ceci est une \n question test \\ retour à al alinge...",
#             "lines":3
#         }
#     }
#     res=renderjinja("qcmgen","resources/amc_elements_templates","open-question.tex.jinja",d)
#     print(res)


@main.command()
@click.argument('folder',default=".")
@click.option('--filename', default='question_randomized.tex',help="nom du fichier de question à générer au format latex")
def grq(filename:str,folder:str):
    """Generate randomized questions - Lance le script de génération automatique de questions aléatoires depuis le script 
    du repertoire question-builder (implémenter la génération des questions dans le fichier question-builder.generate.py)
    doit être executé depuis un repertoire projet AMC
    """

    try:
        projdir=get_curr_project_dir(folder)
        
        # charge dynamiquement le script
        genscript=projdir/"question-builder"/"generate.py"
        if not genscript.exists():
            raise UserError("can't find python question-builder/generate.py script. ensure that the AMC project has been build with `qcm init`")

        generate_module=import_from_source_file("generate",genscript)
        
        # lance l'execution du script
        generate_module.process_questions(projdir,filename)
    except UserError as e:
        print_error(e.message)



if __name__ == '__main__':
    main()
