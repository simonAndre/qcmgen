# qcmgen: Générateur de QCM AMC 

Ce programme, piloté par le script qcm.py permet:

- d'initialiser un projet personnalisé de questionnaire basé sur auto-multiple-choice (AMC)
- de générer des questions sur une base aléatoire par des scripts python simples.


générateur de questions au format auto-multiple-choice/Latex permettant d'automatiser la création de questions aléatoires.

[documentation AMC](https://download.auto-multiple-choice.net/auto-multiple-choice.en.pdf)

## Usage

`./qcm.py -h`

il est conseillé de faire un alias pour disposer d'une commander `qcm` pointant vers le script `qcm.py`

### intialisation d'un projet AMC

ex: 
```bash
qcm.py init my_amc_project
# ==> créer un repertoire DS_1 avec toute la structure de fichiers nécessaire pour une personnalisation des questions
```
structure du projet créé par la commande `qcm init my_amc_project`:
```
my_amc_project
├── amc-compiled.amc
├── amc-compiled.aux
├── amc-compiled-config.tex
├── amc-compiled.log
├── amc-compiled.pdf
├── amc-form-cartouche.tex
├── amc-form-preambule.tex
├── anonymous
├── copies
├── cr
│   ├── corrections
│   │   ├── jpg
│   │   └── pdf
│   ├── diagnostic
│   └── zooms
├── data
│   ├── association.sqlite
│   ├── capture.sqlite
│   ├── layout.sqlite
│   ├── report.sqlite
│   └── scoring.sqlite
├── DOC-calage.xy
├── DOC-corrige.pdf
├── DOC-sujet.pdf
├── exports
├── options.xml
├── question-builder
│   ├── generate.py
│   └── README.md
├── sample_questiongroups.tex
├── scans
└── source.tex
```

#### templates déployés à l'initialisation des projet AMC

- le template d'initialisation du repertoire de la structure de projet AMC est personnalisable dans `./qcmgen/resources/amc_bootstrap_template`.
    
    Le contenu de ce repertoire est encapsulé dans le package python `qcmgen` et déployé par la commande `qcm init`.
    
    Ce template contient tous les fichiers paramétrables d'un projet AMC: 
    ```
    amc_bootstrap_template
    ├── amc-form-cartouche.tex
    ├── amc-form-preambule.tex
    ├── options.xml
    ├── sample_questiongroups.tex
    └── source.tex
    ```


- lors de l'utilisation de la commande `qcm init`, le répertoire `[projet_AMC]/question-builder` est également déployé. il contient le script "modèle" de génération des questions aléatoirisées. Les sources de ce repertoire  se trouvent dans: `./qcmgen/resources/question-builder`.


### génération des question aléatoirisées

ex: 
```bash
qcm.py grq my_amc_project
```

Cette commande aura pour effet d'executer le script `my_amc_project/question-builder/generate.py` pour générer les questions aléatoirisées dans le fichier `question_randomized.tex` (le nom du fichier est surchargeable par les options de la commande `qcm grq`)

### lancer l'IHM d'AMC

ex: 
```bash
qcm.py amc my_amc_project
```

### Mettre à jour les document

la commande `reapply` relance la génération des documents PDF (équivalent du bouton "update documents" sur l'IHM d'AMC).

Attention, l'examen ne doit pas avoir déjà été imprimé et distribué car tous les paramètres de scann des réponses aux question sont modifiés.

## Build

utiliser le Makefile.

pour builder et copier le package sur le "repo local": `make all`

