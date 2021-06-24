import os
import numpy as np
#from shutil import copyfile
from andes_run_amr2cube import get_header_txt,get_run_txt




in_path = "/gpfs/alpine/proj-shared/ast031/pocvirk/CoDaIII/prod_sr/"
out_path = "/gpfs/alpine/proj-shared/ast031/jlewis/CoDaIII/prod_sr/amr2cube_runs/"


type_ints=[1,8]
types = ['amr','rho','vx','vy','vz','temp','Z','dust','xion','J21'] #if in doubt, check the hydro_file_descriptor.txt file of a snapshot


#get_outputs                                                                                             
#outputs = [elem for elem in os.listdir(out_path) if 'output' in elem]
#output_paths = [os.path.join(out_path,elem) for elem in outputs]
#out_paths = [os.path.join(out_path,elem) for elem in outputs]
outputs=['000080','000101']
out_paths = [os.path.join(out_path,'output_%s'%elem) for elem in outputs]
in_paths = [os.path.join(in_path,'output_%s'%elem) for elem in outputs]

print('************************************************************')
print('Extracting %s in %s'%(types[type_int],', '.join(outputs)))
print('************************************************************\n\n')

nodes=1
ntaskspn=32 #32 cores per node on ANDES so there should be a task per core

sub_nb=0
frac=1./16
Nfrac=int(np.round(1/frac))
Njobs=1 #number of .slurm scripts we need to make
Ntasks_per_job= Nfrac**3 #per output

tot_time_mm = 0.77*Ntasks_per_job #1.3 boites de 512^3 (Nfrac =16) par min avec 32 cores par noeuds travaillant en parallel

hh,mm,ss = tot_time_mm//60,tot_time_mm%60,0

overstep=hh>=48

if overstep:
    print('WARNING: Overstepped maximum walltime for one node, dividing job into several .slurm files')

    Njobs=np.int(np.ceil(hh/48))
    Ntasks_per_job=int(np.ceil(Ntasks_per_job/Njobs))
    hh,mm,ss=48,00,00

for type_int in type_ints:    
    
        for output,in_path,output_path in zip(outputs,in_paths,out_paths):

            ijob=0

            fname = 'extract_%s_%s_%i.slurm'%(types[type_int],output,ijob)

            pbs_file=open(os.path.join('.',fname),'w')

            hdr=get_header_txt(out_path,nodes,ntaskspn,hh,mm,ss)

            pbs_file.write(hdr)


            if not os.path.isdir(out_path) : os.makedirs(output_path)

            print('Found %s, queueing amr2cube ...'%output)


            for xfrac in range(Nfrac):
                for yfrac in range(Nfrac):
                    for zfrac in range(Nfrac):

                        #use this if for some reason some tasks didn't complete (add the sub_nb/task nb in this list and uncomment
                        # if sub_nb not in [552,558,559,574,575,627,628,643,644,666,686,687,702,703,814,815,830,831,883,884,899,900,942,943,958,959,1349,1570,1571,1586,1587,1766,1767,1782,1783,1826,1827,1828,1842,1843,1844,2022,2023,2038,2039,2083,2084,2099,2100,2200,2314,2675,2676,2691,2692,2878,2879,2894,2895,2931,2932,2947,2948,3006,3007,3022,3023,3134,3135,3150,3151,3262,3263,3278,3279,3313,3584,3591,3592,3599,3703,3704,3719,3720,3814,3815,3824,3830,3831,3832,3839,3840,3846,3847,3848,3855,3943,3944,3959,3960,3975,3976,4070,4071,4072,4080,4086,4087,4088,4095] :
                        #     sub_nb+=1
                        #     continue

                        xmin,xmax=xfrac*frac,(xfrac+1)*frac
                        ymin,ymax=yfrac*frac,(yfrac+1)*frac
                        zmin,zmax=zfrac*frac,(zfrac+1)*frac                    

                        write_path=os.path.join(out_path,'output_%s'%output,'%s_%05d'%(types[type_int],sub_nb))

                        amr2cube_line=get_run_txt(in_path,write_path,type_int,types[type_int],xmin,xmax,ymin,ymax,zmin,zmax)
                        pbs_file.write(amr2cube_line)

                        sub_nb+=1

                        if sub_nb%ntaskspn==0:pbs_file.write('wait\n') #needed or we exit without some jobs being run!

                        if sub_nb%Ntasks_per_job==0:
                            print('triggered, %i, %i'%(sub_nb,Ntasks_per_job))

                            pbs_file.write('wait\n')
                            pbs_file.write("echo 'job done'")
                            pbs_file.close()

                            ijob+=1

                            fname = 'extract_%s_%s_%i.slurm'%(types[type_int],output,ijob)
                            pbs_file=open(os.path.join('.',fname),'w')	

                            pbs_file.write(hdr)


            pbs_file.write('wait\n')
            pbs_file.write("echo 'job done'")
            pbs_file.close()

                    
#exec_file = os.path.join(out_path,'amr2cube_andes')
#copyfile('amr2cube_andes',exec_file)
#os.system('chmod 777 %s'%exec_file)
#cmd='sbatch %s'%os.path.join(out_path,fname)
#print(cmd)
#os.system(cmd)
