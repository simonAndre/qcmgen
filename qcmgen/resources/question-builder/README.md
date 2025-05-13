# Generation de questions au format AMC

[documentation AMC](https://download.auto-multiple-choice.net/auto-multiple-choice.en.pdf)

Ce projet contient un script python permettant de générer une fichier latex au format AMC avec des groupes de questions "aléatoirisées" :

Utilisation: ./generate.py [AMC_project_dir] [questiongroup.tex]
    avec:
    - [AMC_project_dir]: repertoire projet AMC
    - [questiongroup.tex]: fichier latex du groupe de questions AMC à générer

exemple: `./generate.py .. questions_alea.tex`

## Prerequis

Requière le paquet python [qcmgen](https://github.com/simonAndre/qcmgen)