import re
import importlib.resources
from pathlib import Path
from .common.utils import UserError
from .common.jinja_templating import renderjinja
from .amc_commands import prepare_project
SUBFOLDERS = [
    "cr",
    "cr/corrections",
    "cr/corrections/jpg",
    "cr/corrections/pdf",
    "cr/diagnostic",
    "cr/zooms",
    "data",
    "exports",
    "scans",
    "copies",
]


def renderjinjaresources(sourcedir,outpath,data):
    """extrait les fichiers des templates jinja localisés dans le reptoire ressources.

    Args:
        outpath (_type_): repertoire de destination des fichiers générés à partir des templates jinja
        data (_type_): _description_
    """
    prj_folder = Path(outpath)
    for fi in importlib.resources.files(sourcedir).iterdir():
        if fi.is_file() and fi.name.endswith(".jinja"):
            try:
                contenu=renderjinja("qcmgen","resources/amc_bootstrap_template",fi.name,data)
                print(f"generation du fichier {fi.name}")
                # l'extension .jinja est retirée du nom de fichier pour crérer le fichier de destinataiton
                outfilename=re.sub(r'\.jinja$','',fi.name)
                with (prj_folder/outfilename).open("w", encoding="utf-8") as outf:
                    outf.write(contenu)
            except Exception as e:
                raise ValueError(f"erreur dans le rendu du template {fi.name}") from e


def get_curr_project_dir(folder:str="."):
    """retourne le repertoire du projet en validant qu'il s'agit bien d'un repertoire AMC

    args: 
        - folder: si définit: chemin du projet (sinon, teste le chemin courant)
    """
    # on teste la présence d'un fichier options.xml (ça suffit pour l'instant)
    if (Path(folder)/"options.xml").exists():
        return Path(folder).absolute()
    else:
        raise UserError("Can't find any proper AMC project. Ensure that the AMC project has been build with `qcm init`")

def copy_embedd_data(sourcedir,outpath):
    """copie des fichiers encapsulés dnas le package dans le repertoire sourcedir 
    vers le répertoire outpath
    """
    for fi in importlib.resources.files(sourcedir).iterdir():
        if fi.is_file() and not fi.name.endswith(".jinja"):
            print(f"copie du fichier {fi.name}")
            with (fi.open("r", encoding="utf-8") as f):
                contenu = f.read()
                with (outpath/fi.name).open("w", encoding="utf-8") as outf:
                    outf.write(contenu)

def copy_amcsources(outpath,projectdata):
    """copie les fichiers contenus dans le repertoire qcmgen.resources.amc_bootstrap_template du package
    vers le répertoire outpath
    """
    copy_embedd_data("qcmgen.resources.amc_bootstrap_template",outpath)
    renderjinjaresources("qcmgen.resources.amc_bootstrap_template",outpath,projectdata)



def copy_questionbuilder_script(outpath):
    """copie le modèle de script python pour générer des questions aleatoirisées
    vers le répertoire outpath
    """
    folder=(outpath/"question-builder")
    folder.mkdir()
    copy_embedd_data("qcmgen.resources.question-builder",folder)

def create_gitignore(outpath):
    with (outpath/".gitignore").open("w", encoding="utf-8") as outf:
        outf.write(
            """*
!DOC-sujet.pdf
!.gitignore
!*.tex""")


def create_project_structure(folder, overwrite,projectdata):
    """
    crée le repertoire AMC à partir de la structure de projet par défaut et 
    des fichiers templates contenus dans le repertoire qcmgen.resources.amc_bootstrap_template 
    du présent package
    """

    def __addcontent(outpath):
        copy_amcsources(prj_folder,projectdata)
        copy_questionbuilder_script(prj_folder)
        create_gitignore(prj_folder)
        prepare_project(prj_folder)
    
    prj_folder = Path(folder)
    if not prj_folder.exists():
        prj_folder.mkdir()
        for sf in SUBFOLDERS:
            (prj_folder / sf).mkdir()
        print(f"répertoire {folder} créé")
        __addcontent(prj_folder)
    else:
        if overwrite:
            __addcontent(prj_folder)
        else:
            UserError(f"rép {folder} existe déjà")
