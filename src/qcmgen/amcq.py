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
    def __init__(self, question_text: str, qutype,template, points, scoringfunc=""):
        self._qutext = question_text
        self._scoringfunc = scoringfunc
        self._points = points
        self._template = template
        self._element = {
            "group_name": "",
            "preambule": "",
            "postambule": "",
            "content": "",
        }
        self._questiondata = {
            "questionid": None,
            "questiontype":qutype,
            "maxpoints": points,
            "lines": 1,
            "content": question_text,
            "multicols":1,
            "choices":[],
            # "resolver":{"questiontype":lambda type: embrace("question" if type=="simple" else "questionmult")}
        }        

    def add_preambule(self, preambule):
        self._element["preambule"] = preambule

    def add_postambule(self, postambule):
        self._element["preambule"] = postambule

    def render_item(self, template, data):
        return renderjinja("qcmgen", "resources/amc_elements_templates", template, data)

    def add_choice(self,text,correct):
        self._questiondata["choices"].append({"correct":correct,"text":text})

    def process(self, group_name, question_number):
        assert self._points is not None, (
            f"Les points de la question {question_number} n'ont pas été définits. Vous pouvez définir les points sur chaque question ou globalement sur le groupe de question"
        )
        assert question_number is not None,"question_number must be defined"
        self._questiondata["questionid"]=question_number
        self._questiondata["maxpoints"]=self._points
        questionContent=self.render_item(self._template,self._questiondata)
        self._element["content"]=questionContent
        return self.render_item("element.tex.jinja", self._element)


class QuSingleChoice(Question):
    def __init__(
        self,
        question_text: str,
        cols: int = 1,
        qutype="question",
        points=None,
        scoringfunc="sanbar",
    ):
        super().__init__(question_text, qutype, points, scoringfunc=scoringfunc,template="question-close.tex.jinja")
        self._questiondata["multicols"] = cols

    def add_choice(self, value: str, is_correct: bool):
        super().add_choice(value, is_correct)

    def process(self, group_name, question_number):
        return super().process(group_name, question_number)


class QuMultipleChoice(QuSingleChoice):
    def __init__(self, question_text: str, cols: int = 1, points=None):
        super().__init__(
            question_text,
            cols,
            qutype="questionmult",
            points=points,
            scoringfunc="sanbarm",
            template="question-close.tex.jinja"
        )


class QuOpen(Question):
    """Question open (saisie libre du résultat)"""

    def __init__(self, question_text: str, lines: int, points=None):
        assert lines
        super().__init__(
            question_text, qutype="question",template="question-open.tex.jinja", points=points, scoringfunc="sanbar"
        )
        self._questiondata["lines"]=lines

    def process(self, group_name, question_number):
        self._line2 = f"\\begin{{{self._qutype}}}{{%qunumber%}}"
        return super().process(group_name, question_number)


# TODO:
#  d={
#         "amcq":{
#             "maxpoints":4,
#             "questionid":"qtest-1",
#             "content":"ceci est une \n question test \\ retour à al alinge...",
#             "lines":3
#         }
#     }
#     res=renderjinja("qcmgen","resources/amc_elements_templates","question-open.tex.jinja",d)


class QuestionGroup:
    """Groupe de questions homogène. pour rendre aléatoires les composantes d'une question,
    on créée sous le meme groupe de question plusieurs versions de la question en randomisant
    l'énoncée et les réponses en lien avec l'énoncé.

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
        self._questions = []
        self._preambule = ""
        self._postambule = ""

    def add_rule_before(self):
        """ajoute une ligne horizontale avant chaque question"""
        self._preambule = "\n\\begin{center}\\rule{4cm}{0.4pt}\\end{center}"

    def add_rule_after(self):
        """ajoute une ligne horizontale après chaque question"""
        self._postambule = "\\begin{center}\\rule{4cm}{0.4pt}\\end{center}\n"

    def add_question(self, question: Question):
        if question._points is None:
            question._points = self._points
        question.add_preambule(self._preambule)
        question.add_postambule(self._postambule)
        self._questions.append(question)

    def process(self):
        print(
            f"génération du groupe de question {self._group_name} ({len(self._questions)} questions)"
        )
        body = f"% *** Groupe de question {self._group_name} ***\n% pour insérer une question tirée aléatoirement depuis ce groupe, utiliser \\insertgroup[1]{{{self._group_name}}}\n"

        for num, question in enumerate(self._questions):
            question_number = f"{self._group_name}-{num}"
            body += (
                question.process(
                    group_name=self._group_name, question_number=question_number
                )
                + "\n"
            )
        body += f"% pour mélanger aléatoirement les questions du groupe de question\n\\setgroupmode{{{self._group_name}}}{{withreplacement}}\n\n"
        return body


class QuestionsFile:
    """représente un fichier de groupes de questions"""

    def __init__(self, folder, filename):
        self._qg = []
        self._folder = folder
        self._filename = filename

    def add_questiongroup(self, qg):
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
