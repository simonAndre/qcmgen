# amcq:  AMC questions types
from pathlib import Path
from collections import namedtuple

Choice=namedtuple('Choice',['value','is_correct'])

class Question:
    def __init__(self,question_text:str,qutype,points,scoringfunc=""):
        self._qutext=question_text
        self._qutype=qutype
        self._points=points
        self._scoringfunc=scoringfunc
        self._body=""
        self._line2=f"\\begin{{{self._qutype}}}{{%qunumber%}}\\{self._scoringfunc}{{%qupoints%}}"
    def process(self,body,group_name,question_number):
        assert self._points is not None,f"Les points de la question {question_number} n'ont pas été définits. Vous pouvez définir les points sur chaque question ou globalement sur le groupe de question"
        line2=self._line2.replace("%qunumber%",question_number).replace("%qupoints%",str(self._points))
        return f"\\element{{{group_name}}}{{\n\t{line2}\n{self._qutext}\n\t\t{body}\n\t\\end{{{self._qutype}}}\n}}"

class QuSingleChoice(Question):
    def __init__(self,question_text:str,cols:int=1,qutype="question",points=None,scoringfunc="sanbar"):
        super().__init__(question_text,qutype,points,scoringfunc=scoringfunc)
        self._cols=cols
        self._choices=[]
    def add_choice(self,value:str,is_correct:bool):
        self._choices.append(Choice(value,is_correct))
    def process(self,group_name,question_number):
        body= f"""\\begin{{multicols}}{{{self._cols}}}
            \\begin{{choices}}\n"""
        for c in self._choices:
            if c.is_correct:
                body+=f"\t\t\t\t\\correctchoice{{{c.value}}}\n"
            else:
                body+=f"\t\t\t\t\\wrongchoice{{{c.value}}}\n"
        body+="""\t\t\t\\end{choices}
        \\end{multicols}"""
        return super().process(body,group_name,question_number)

class QuMultipleChoice(QuSingleChoice):
    def __init__(self,question_text:str,cols:int=1,points=None):
        super().__init__(question_text,cols,qutype="questionmult",points=points,scoringfunc="sanbarm")

class QuOpen(Question):
    """Question open (saisie libre du résultat)
    """
    def __init__(self,question_text:str,lines:int,points=None):
        assert lines
        self._lines=lines
        super().__init__(question_text,qutype="question",points=points,scoringfunc="sanbar")
    def process(self,group_name,question_number):
        self._line2=f"\\begin{{{self._qutype}}}{{%qunumber%}}"
        body=f"\\ph{{{self._lines}}}{{{self._points}}}"
        return super().process(body,group_name,question_number)
   

class QuestionGroup:
    """Groupe de questions homogène. pour rendre aléatoires les composantes d'une question, 
    on créée sous le meme groupe de question plusieurs versions de la question en randomisant 
    l'énoncée et les réponses en lien avec l'énoncé.

    pour insérer une des questions du groupe de question, on utilise la commande \\insertgroup[1]{nom-groupe}
    le [1] précise qu'une question sera tirée aléatoirement dans le groupe 
    """
    def __init__(self,points:int,group_name:str):
        """_summary_

        Args:
            points (int): nb de points des questions du groupe de question
            group_name (str): libellé du groupe de question
        """
        self._points=points
        self._group_name=group_name
        self._questions=[]
    
    def add_question(self,question:Question):
        if question._points is None:
            question._points=self._points
        self._questions.append(question)

    def process(self):
        print(f"génération du groupe de question {self._group_name} ({len(self._questions)} questions)")
        body=f"% *** Groupe de question {self._group_name} ***\n% pour insérer une question tirée aléatoirement depuis ce groupe, utiliser \\insertgroup[1]{{{self._group_name}}}\n"
        
        for num,question in enumerate(self._questions):
            question_number=f"{self._group_name}-{num}"
            body+=question.process(group_name=self._group_name, question_number=question_number)+"\n"
        body+=f"% pour mélanger aléatoirement les questions du groupe de question\n\\setgroupmode{{{self._group_name}}}{{withreplacement}}\n\n"
        return body
  

class QuestionsFile:
    """représente un fichier de groupes de questions
    """
    def __init__(self,folder,filename):
        self._qg=[]
        self._folder=folder
        self._filename=filename

    def add_questiongroup(self,qg):
        self._qg.append(qg)

    def flush(self):
        amc_folder=Path(self._folder)
        if not amc_folder.exists():
            amc_folder.mkdir()
        amc_main_file=amc_folder / self._filename
        
        content=""
        for qg in self._qg:
            content+=qg.process()
        
        with open(amc_main_file,"w") as f:
            f.write(content)
            print(f"""
>>> fichier {amc_main_file} correctement créé,
pour importer les questions du fichier, dans le fichier latex ppal: source.tex :
- importez le fichier de questions: \input{{{amc_main_file}}}
- insérer le ou les groupes de questions correspondant, ex pour insérer 1 question du groupe: \insertgroup[1]{{groupename}}""")



