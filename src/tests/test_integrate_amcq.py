from qcmgen.amcq import QuestionsFile,QuOpen,QuestionGroup,QuSingleChoice,QuMultipleChoice

def test_render_single_questions():
    quopen=QuOpen("open question 1",3,2)
    res=quopen.process("openqu_1")
    print(res)
    expected=r"""\begin{question}{openqu_1}
    (2 pts) open question 1
    \AMCOpen{lines=3,dots=false,question=openqu_1}{
        \wrongchoice[F]{f}
        \scoring{0}
        \wrongchoice[P]{p}
        \scoring{1}
        \correctchoice[J]{j}
        \scoring{2}
    }    
\end{question}"""

    assert res==expected



def test_render_file1():
    qfile=QuestionsFile("./src/tests/out","test_out1.tex")
    qg1=QuestionGroup(3,"groupe1")
    quopen1=QuOpen("open question 1",3,2,question_id="quopen1")
    qg1.add_question(quopen1)
    qfile.add_questiongroup(qg1)

    qg2=QuestionGroup(3,"groupe2")
    quopen2=QuOpen("open question 2",3,2,question_id="quopen2")
    qg2.add_question(quopen2)
    qfile.add_questiongroup(qg2)

    qg3=QuestionGroup(1,"groupe3")
    qg3.add_question(QuOpen("open question 3",1,1))
    qg3.add_question(QuOpen("open question 4",1,1))
    qfile.add_questiongroup(qg3)
    qfile.add_single_question(QuSingleChoice("sipgnle choice quest 1",2,1))


    qfile.flush()