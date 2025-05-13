import subprocess
from pathlib import Path
def prepare_project(amcprojdir,tex_source_filename="source.tex"):
    # à ne pas refaire une fois les copies imprimées
	
    # auto-multiple-choice prepare --mode s ${projdir}/source.tex \
	# --out-sujet DOC-sujet.pdf --out-corrige DOC-corrige.pdf --out-calage DOC-calage.xy \
	# --with pdflatex --data ${projdir}/data
    try:
        result=subprocess.run(['auto-multiple-choice', 'prepare',
        '--mode', 's',str((amcprojdir / tex_source_filename).absolute()),
        '--out-sujet','DOC-sujet.pdf','--out-corrige','DOC-corrige.pdf','--out-calage','DOC-calage.xy',
        '--with','pdflatex','--data', str((amcprojdir / "data").absolute())
        ], check=True,stdout=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f'Command {e.cmd} failed with error {e.returncode}')


def open_AMC(amcprojdir:Path):
    try:
        result=subprocess.run(['auto-multiple-choice', amcprojdir.absolute().name],cwd=str(amcprojdir/ ".."), check=True,stdout=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f'Command {e.cmd} failed with error {e.returncode}')
