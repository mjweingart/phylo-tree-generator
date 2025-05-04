# Phylogenetic Tree Generator
This is a simple GUI application that generates a phylogenetic tree from protein sequence FASTA files using Clustal Omega for alignment and FastTree for tree construction, with midpoint rooting implemented using the `ete3` library. I'm a mostly self-taught programmer, and this represents my first attempt at building something bioinformatics related.

## Prerequisites
- Python 3.x
- Required libraries: `ete3`, `ttkbootstrap`, `matplotlib`, `Pillow`
- External tools: `clustalo.exe`, `fasttree.exe`, and their dependencies (`libgcc_s_sjlj-1.dll`, `libgomp-1.dll`, `libstdc++-6.dll`, `pthreadGC2-w64.dll`)

## Instructions
- Ensure all of the files in the 'assets' and 'tools' folders are in the same directory as pipeline.py.
- Run pipeline.py.
- Select all of the FASTA files that you wish to be included in the phylogenetic tree. All FASTA files must be in a single directory. In the 'example fasta files' folder are some example FASTA files for the mitochondrial protein cytochrome B. 

## Executable
- I've uploaded an .exe of the app to the releases section for convenience. 
- To package an .exe up yourself using Pyinstaller, use the following command:
  "pyinstaller --onefile  --icon=icon.ico --hidden-import ete3 --hidden-import matplotlib --hidden-import ttkbootstrap --noconsole pipeline.py --add-binary "clustalo.exe;." --add-binary "fasttree.exe;." --add-binary "libgcc_s_sjlj-1.dll;." --add-binary "libgomp-1.dll;." --add-binary "libstdc++-6.dll;." --add-binary "pthreadGC2-w64.dll;." --add-data "icon.ico;." --add-data "Tree Background pic resized.png;." --upx-dir . --exclude-module PySide2 --exclude-module IPython --exclude-module scipy".
