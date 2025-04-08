import subprocess
import os

def makeRecon(AO_path, sMatrixDir,imageDir,reconExe):

    # Check if the input file exists
    if not os.path.exists(AO_path):
        print(f"Error: no input file {AO_path}")
        exit(1)

    # Check if the system matrix directory exists
    if not os.path.exists(sMatrixDir):
        print(f"Error: no system matrix directory {sMatrixDir}")
        exit(2)

    # Create the output directory if it does not exist
    os.makedirs(imageDir, exist_ok=True)

    opti = "MLEM"
    penalty = ""
    iteration = "100:10"

    cmd = (
        f"{reconExe} -df {AO_path} -opti {opti} {penalty} "
        f"-it {iteration} -proj matrix -dout {imageDir} -th 24 -vb 5 -proj-comp 1 -ignore-scanner "
        f"-data-type AOT -ignore-corr cali,fdur -system-matrix {sMatrixDir}"
    )
    result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
    print(result.stdout)