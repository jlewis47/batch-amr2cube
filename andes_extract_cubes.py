import os
import numpy as np
from shutil import copyfile
from andes_run_amr2cube import get_header_txt,get_run_txt




in_path = "/gpfs/alpine/proj-shared/ast031/pocvirk/CoDaIII/prod_sr/"
out_path = "/gpfs/alpine/proj-shared/ast031/jlewis/CoDaIII/prod_sr/amr2cube_runs/"


type_int=1
types = ['amr','rho','vx','vy','vz','temp','Z','dust','xion','J21'] #if in doubt, check the hydro_file_descriptor.txt file of a snapshot


#get_outputs                                                                                             
#outputs = [elem for elem in os.listdir(out_path) if 'output' in elem]
#output_paths = [os.path.join(out_path,elem) for elem in outputs]
#out_paths = [os.path.join(out_path,elem) for elem in outputs]
outputs=['000080']
out_paths = [os.path.join(out_path,'output_%s'%elem) for elem in outputs]
in_paths = [os.path.join(in_path,'output_%s'%elem) for elem in outputs]

print('************************************************************')
print('Extracting %s in %s'%(types[type_int],', '.join(outputs)))
print('************************************************************\n\n')



sub_nb=0
frac=1./16
Nfrac=int(np.round(1/frac))


tot_time_mm = 5*len(outputs)*Nfrac**3 #1min par fichier

hh,mm,ss = tot_time_mm//60,tot_time_mm%60,0


if hh>=48:
    print('WARNING: Overstepped maximum walltime for one node, setting walltime to maximum')
    hh,mm,ss=48,00,00
    
nodes=1
ntaskspn=1



fname = 'extract_%s_%s.slurm'%(types[type_int],', '.join(outputs))


with open(os.path.join('.',fname),'w') as pbs_file:

    hdr=get_header_txt(out_path,nodes,ntaskspn,hh,mm,ss)

    pbs_file.write(hdr)


    for output,in_path,output_path in zip(outputs,in_paths,out_paths):
                    
        if not os.path.isdir(out_path) : os.makedirs(output_path)

        print('Found %s, queueing amr2cube ...'%output)

    
        for xfrac in range(Nfrac):
            for yfrac in range(Nfrac):
                for zfrac in range(Nfrac):
                

                    xmin,xmax=xfrac*frac,(xfrac+1)*frac
                    ymin,ymax=yfrac*frac,(yfrac+1)*frac
                    zmin,zmax=zfrac*frac,(zfrac+1)*frac                    

                    write_path=os.path.join(out_path,'%s_%05d'%(types[type_int],sub_nb))
                    
                    amr2cube_line=get_run_txt(in_path,write_path,type_int,types[type_int],xmin,xmax,ymin,ymax,zmin,zmax)
                    pbs_file.write(amr2cube_line)

                    sub_nb+=1
                    



#exec_file = os.path.join(out_path,'amr2cube_andes')
#copyfile('amr2cube_andes',exec_file)
#os.system('chmod 777 %s'%exec_file)
#cmd='sbatch %s'%os.path.join(out_path,fname)
#print(cmd)
#os.system(cmd)
