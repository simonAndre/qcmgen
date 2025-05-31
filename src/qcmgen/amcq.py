# amcq:  AMC questions types
from pathlib import Path
from .common.jinja_templating import renderjinja
from collections import namedtuple

Choice = namedtuple("Choice", ["value", "is_correct"])

amcTemplates={
    "qu-close":"question-close.tex.jinja",
    "qu-open":"question-open.tex.jinja",
    "element":"element.tex.jinja",
}

class Question:
    def __init__(self, question_text: str, qutype, points, scoringfunc="",question_id=None):
        self._qutext = question_text
        self._points = points
        self._question_id=question_id
        self._questiondata = {
            "questionid": None,
            "questiontype":qutype,
            "maxpoints": points,
            "lines": 1,
            "content": question_text,
            "multicols":1,
            "questionid":question_id,
            # "resolver":{"questiontype":lambda type: embrace("question" if type=="simple" else "questionmult")}
        }     

    @property
    def template(self):
        "template jinja à utiliser pour générer la question"
        return self._template
    @template.setter
    def template(self,value):
        self._template=value

    def process(self, question_id):
        assert self.template,"template must be defined"
        assert self._points is not None, (
            f"Les points de la question {question_id} n'ont pas été définits. Vous pouvez définir les points sur chaque question ou globalement sur le groupe de question"
        )
        if not self._question_id:
            assert question_id is not None,"question_id must be defined"
            self._question_id=question_id
        self._questiondata["questionid"]=self._question_id
        self._questiondata["maxpoints"]=self._points
        return renderjinja("qcmgen", "resources/amc_elements_templates", self._template,self._questiondata)


class QuSingleChoice(Question):
    def __init__(
        self,
        question_text: str,
        cols: int = 1,
        points=None,
        question_id=None,
        qutype="question",
    ):
        super().__init__(question_text, qutype, points, question_id=question_id)
        self._questiondata["multicols"] = cols
        self._questiondata["choices"] = []
        self.template="question-close.tex.jinja"

    def add_choice(self, text: str, is_correct: bool,feedback:str):
        # TODO: handle feedback
        self._questiondata["choices"].append({"correct":is_correct,"text":text})

    def process(self, question_id=None):
        return super().process(question_id)


class QuMultipleChoice(QuSingleChoice):
    def __init__(self, question_text: str, cols: int = 1, points=None):
        super().__init__(
            question_text,
            cols,
            qutype="questionmult",
            points=points,
        )
        self.template="question-close.tex.jinja"


class QuOpen(Question):
    """Question open (saisie libre du résultat)"""

    def __init__(self, question_text: str, lines: int, points=None,question_id=None):
        """Question open (saisie libre du résultat)

        Args:
            question_text (str): texte de la question
            lines (int): nombre de lignes du cadre de réponse
            points (_type_, optional): nb de points max. Defaults to None.
        """
        assert lines
        super().__init__(
            question_text, qutype="question", points=points,question_id=question_id
        )
        self._questiondata["lines"]=lines
        self.template="question-open.tex.jinja"


    def process(self, question_id=None):
        return super().process(question_id)

class Element:
    def __init__(self,name=None):
        self._elementdata={
            "name": name,
            "addruleafer":False,
            "addrulebefore":False,
            "preambule":"",
            "postambule":"",
            "content": "",
        }
        self._questions = []

    def add_question(self, question: Question):
        if not self._elementdata["name"]:
            assert question._question_id, "si aucun nom n'est définit pour un élément, il est extrait à partir de l'id de la première question qui doit être définit"
            self._elementdata["name"]=question._question_id
        self._questions.append(question)
   
    def add_rule_before(self):
        """ajoute une ligne horizontale avant chaque question"""
        self._elementdata["addrulebefore"]=True

    def add_rule_after(self):
        """ajoute une ligne horizontale après chaque question"""
        self._elementdata["addruleafter"]=True

    def process(self):
        content=""
        for qu in self._questions:
            content+=qu.process()+"\n"
        self._elementdata["content"]=content
        return renderjinja("qcmgen", "resources/amc_elements_templates", "element.tex.jinja",self._elementdata)


class QuestionGroup:
    """Groupe de questions homogène. pour rendre aléatoires les composantes d'une question,
    on créée sous le meme groupe de question plusieurs versions de la question en randomisant
    l'énoncée et les réponses en lien avec l'énoncé.

    Dans un groupe de "questions aléatoirisées", chaque version de la question est insérée dans un élément, 
    tous les éléments de versions de question ont le même nom.

    pour insérer une des questions du groupe de question, on utilise la commande \\insertgroup[1]{nom-groupe}
    le [1] précise qu'une question sera tirée aléatoirement dans le groupe
    """

    def __init__(self, points: int, group_name: str):
        """_summary_

        Args:
            points (int): nb de points des questions du groupe de question
            group_name (str): libellé du groupe de question
        """
        self._points = points
        self._group_name = group_name
        self._data={
            "group_name":group_name,
            "content":"",
            "elements":[]
        }
        self._elements = []
        self._isolatedquestionsnumber=0


    def add_element(self, element: Element):
        self._elements.append(element)

    def add_question(self, question: Question):
        self._isolatedquestionsnumber+=1
        if question._points is None:
            question._points = self._points
        if not question._question_id:
            question._question_id=f"{self._group_name}-{self._isolatedquestionsnumber}"
        element=Element(self._group_name)
        element.add_question(question)
        self.add_element(element)

    def process(self):
        print(
            f"génération du groupe de question {self._group_name} ({len(self._elements)} elements)"
        )
        for element in self._elements:
            self._data["elements"].append(element)
            self._data["content"] += (
                element.process()
                + "\n"
            )
        return renderjinja("qcmgen", "resources/amc_elements_templates", "group-questions.tex.jinja",self._data)


class QuestionsFile:
    """représente un fichier de groupes de questions"""

    def __init__(self, folder, filename):
        self._qg = []
        self._folder = folder
        self._filename = filename
        self._isolatedquestiongroupnumber=0


    def add_questiongroup(self, qg:QuestionGroup):
        self._qg.append(qg)
    def add_single_question(self, qu:Question):
        assert qu._points,"points are not defined"
        if not qu._question_id:
            self._isolatedquestiongroupnumber+=1
            qu._question_id=f"questiongroup-{self._isolatedquestiongroupnumber}"
        qg=QuestionGroup(qu._points,qu._question_id)
        qg.add_question(qu)
        self._qg.append(qg)

    def flush(self):
        amc_folder = Path(self._folder)
        if not amc_folder.exists():
            amc_folder.mkdir()
        amc_main_file = amc_folder / self._filename

        content = ""
        for qg in self._qg:
            content += qg.process()

        with open(amc_main_file, "w") as f:
            f.write(content)
            print(f"""
>>> fichier {amc_main_file} correctement créé,
pour importer les questions du fichier, dans le fichier latex ppal: source.tex :
- importez le fichier de questions: \input{{{amc_main_file}}}
- insérer le ou les groupes de questions correspondant, ex pour insérer 1 question du groupe: \insertgroup[1]{{groupename}}""")
