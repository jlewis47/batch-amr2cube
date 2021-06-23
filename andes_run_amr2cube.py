import os

def get_header_txt(path,nodes=1,ntaskspn=8,hh=1,mm=0,ss=0):

 out="#! /bin/bash -l\n#SBATCH -A AST031\n#SBATCH -J amr2cube\n#SBATCH --nodes={1:d}\n#SBATCH --ntasks-per-node={2:d}\n#SBATCH --time {3:02d}:{4:02d}:{5:02d}\n#SBATCH -e slurm-%j.err\n#SBATCH -o slurm-%j.out\nmodule load pgi\necho 'Starting mar2cubes'\necho 'launching aprun'\n".format(path,nodes,ntaskspn,hh,mm,ss)

 return(out)


def get_run_txt(src_path,out_path,typeint,typename,xmi,xma,ymi,yma,zmi,zma):

 out="srun -n 1 --cpus-per-task 1   --cpu-bind cores ./amr2cube_summit -inp {0:s} -out {2:s} -typ {1:d} -xmi {3:f} -xma {4:f} -ymi {5:f} -yma {6:f} -zmi {7:f} -zma {8:f}\n".format(src_path,typeint,out_path,xmi,xma,ymi,yma,zmi,zma)

 return(out)
