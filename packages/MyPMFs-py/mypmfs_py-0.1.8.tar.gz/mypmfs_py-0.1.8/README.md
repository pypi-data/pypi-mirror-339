# MyPMFs_py

The MYPMFs_py Package allows for use of mypmfs training and scoring of the statistical potentials of proteins. Additionally, includes batch download of files from the protein data bank. 

The underlying software package was obtained from https://github.com/bibip-impmc/mypmfs. Please cite the original work (https://doi.org/10.1016/j.biochi.2018.05.013) if you use this package.

# DOWNLOADING MyPMFs_py

The MyPMFs_py package can be installed via pip. Currently only available for Linux.

# DOCUMENTATION

The MyPMFs_py package includes the following functionality

batch_download - batch download of specified, using a csv file of PDB codes, pdb files from the Protein Databank 
can be called with MyPMFs_py.module.batch_download(pdbCodeFile, outputDirPath)
- pdbCodeFile - csv file containing comma seperated PDB codes to be installed
- outputDirPath - directory name for downloaded files

training - executable binary to generate statistical potentials from set of pdb files
can be called with MyPMFs_py.module.training(pdbCodeFile, pdbDirPath, outputDirPath)
- pdbCodeFile - txt files of tab seperated PDB codes to be trained on
- pdbDirPath - path to directory containing PDB files of codes in pdbCodeFile
- outputDirPath - path for output directory of training

scoring - executable binary to generate pseudo-energy of specificed protein based off a pre-generated (using training) set of statistical potenitals 
can be called with MyPMFs_py.module.scoring(pdbFile, potentialsDir)
- pdbFile - specific pdb file to be scored
- potentialsDir - directory containing trained potentials used to score the protein described in pdbFile

# SOURCE CODE

Source Repository: https://github.com/alexhold5/MyPMFs_pypipackage_recipe

# LICENSE

This code is available under the GNU General Public License (see LICENSE.TXT)