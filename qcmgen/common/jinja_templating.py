import jinja2
from .jinja_filters import embrace
def renderjinja(package,packagePath,resname,data):
    """extrait les fichiers des templates jinja localisés dans le reptoire ressources.

    Args:
        outpath (_type_): repertoire de destination des fichiers générés à partir des templates jinja
        data (_type_): _description_
    """
    environment = jinja2.Environment(loader=jinja2.PackageLoader(package,packagePath),trim_blocks=True,lstrip_blocks=True)
    environment.filters["embrace"]=embrace
    jinjatemplate = environment.get_template(resname)
    return jinjatemplate.render(data)
