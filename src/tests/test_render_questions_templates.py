from qcmgen.common.jinja_templating import renderjinja


def test_question_open():
    template = "question-open.tex.jinja"
    questiondata = {
        "questionid": "id1",
        "maxpoints": 3,
        "lines": 2,
        "content": "question_text",
    }
    res = renderjinja("qcmgen", "resources/amc_elements_templates", template, questiondata)
    expected = r"""\begin{question}{id1}
    (3 pts) question_text
    \AMCOpen{lines=2,dots=false,question=id1}{
        \wrongchoice[F]{f}
        \scoring{0}
        \wrongchoice[P]{p}
        \scoring{1}
        \correctchoice[J]{j}
        \scoring{2}
    }    
\end{question}"""
    print(res)
    assert res == expected


def test_questionsimple():
    template = "question-close.tex.jinja"
    questiondata = {
        "questionid": "id1",
        "questiontype":"question",
        "maxpoints": 1,
        "content": "question simple",
        "multicols":2,
        "choices":[
            {"correct":True,"text":"bon choix"},
            {"correct":False,"text":"mauvais choix 1"},
            {"correct":False,"text":"mauvais choix 2"},
            {"correct":False,"text":"mauvais choix 3"},
            {"correct":False,"text":"mauvais choix 4"},
        ]
    }
    res = renderjinja("qcmgen", "resources/amc_elements_templates", template, questiondata)
    print(res)
    expected = r"""\begin{question}{id1}
    (1 pts) question simple
    \begin{multicols}{2}
        \begin{choices}
            \correctchoice{bon choix}
            \wrongchoice{mauvais choix 1}
            \wrongchoice{mauvais choix 2}
            \wrongchoice{mauvais choix 3}
            \wrongchoice{mauvais choix 4}
        \end{choices}
    \end{multicols}
\end{question}"""
    assert res == expected


def test_questionmultiple():
    template = "question-close.tex.jinja"
    questiondata = {
        "questionid": "id2",
        "questiontype":"questionmult",
        "maxpoints": 1,
        "content": "question multiple",
        "multicols":2,
        "choices":[
            {"correct":True,"text":"bon choix 1"},
            {"correct":True,"text":"bon choix 2"},
            {"correct":False,"text":"mauvais choix 1"},
            {"correct":False,"text":"mauvais choix 2"},
            {"correct":False,"text":"mauvais choix 3"},
        ],
        # "resolver":{"questiontype":lambda type: embrace("question" if type=="simple" else "questionmult")}
    }
    res = renderjinja("qcmgen", "resources/amc_elements_templates", template, questiondata)
    print(res)
    expected = r"""\begin{questionmult}{id2}
    (1 pts) question multiple
    \begin{multicols}{2}
        \begin{choices}
            \correctchoice{bon choix 1}
            \correctchoice{bon choix 2}
            \wrongchoice{mauvais choix 1}
            \wrongchoice{mauvais choix 2}
            \wrongchoice{mauvais choix 3}
        \end{choices}
    \end{multicols}
\end{questionmult}"""
    assert res == expected


def test_element():
    template = "element.tex.jinja"
    data = {
        "name": "mygroup",
        "preambule": "",
        "postambule": "",
        "content": "contenu de l'élémet",
    }
    res = renderjinja("qcmgen", "resources/amc_elements_templates", template, data)
    print(res)
    expected = r"""\element{mygroup}{
    contenu de l'élémet
}"""
    assert res == expected
