import subprocess
import os

def training(pdbCodeFile, pdbDirPath, outputDirPath = "data_potentials"):
    path = os.path.join(os.path.dirname(__file__), f"bin/training")
    subprocess.run([path, "-l", pdbCodeFile, "-d", pdbDirPath, "-o", outputDirPath], check=True)

def scoring(pdbFile, potentialsDir):
    path = os.path.join(os.path.dirname(__file__), f"bin/scoring")
    subprocess.run([path, "-i", pdbFile, "-d", potentialsDir], check = True)

def batch_download(pdbCodeFile, outputDirPath):
    os.mkdir(outputDirPath)
    os.chdir(outputDirPath)
    path = os.path.join(os.path.dirname(__file__), f"bin/batch_download.sh")
    subprocess.run([path, "-f", pdbCodeFile, "-p"], check=True)    
    os.system("gzip -d *")
    os.chdir("..")
