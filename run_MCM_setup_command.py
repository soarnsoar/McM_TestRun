import os
import timeit
from SendEmail import SendEmail
import socket
import subprocess
from urllib2 import urlopen






import argparse
#https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/<PREPID>



def convert_arch(script):
  f=open(script,'r')
  fnew=open(script+'_new','w')
  lines=f.readlines()
  for line in lines:
        if 'SCRAM_ARCH' in line and 'slc6' in line:
           line=line.replace('slc6','slc7')
        fnew.write(line)
  f.close()
  fnew.close()
  os.system('mv '+script+'_new '+script)
        

class RunMcM():
    def __init__(self,PREPID,NEVENT):
        self.PREPID=PREPID
        self.NEVENT=NEVENT


    def get_setup_command(self):
        PREPID=self.PREPID
        url = 'https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/'+PREPID


        #response = urlopen(url).read()

        print '--'+PREPID+'--'
        #f = open('setup.sh', "w")
        #print response
        #f.write(response.strip('"').replace('\\n','\n').strip('\n').strip('"'))
        #f.close()
        #os.system('wget '+url)
        os.system('wget --no-check-certificate '+url)
        os.system('mv '+PREPID+' setup.sh')
	#convert_arch('setup.sh')
        os.system('chmod u+x setup.sh')
        #subprocess.call(os.getcwd()+'/setup.sh',shell=True)
        #os.system('source '+os.getcwd()+'/setup.sh')
    def modify_option(self,option,argument):
        PREPID=self.PREPID
        option=' '+option+' '
        #NEVENT=self.NEVENT
        print "--"+str(argument)+"--"
        f=open('setup.sh','r')
        fnew=open('setup.sh_new','w')

        lines=f.readlines()
        for line in lines:
            if option in line:##where defining nevents
                first=line.split(option)[0]
                second=line.split(option)[1]
                second=' '.join(second.split(' ')[1:]) ## remove event value
                newline=first+option+argument+' '+second
                fnew.write(newline)
            else:
                fnew.write(line)
            

        f.close()
        fnew.close()
        os.system('mv setup.sh_new setup.sh')

    def AddCondorJds(self):

        '''
executable = /cms/ldap_home/jhchoi/HWW_Analysis/slc7/ForDevelopHMlnjjSel2017_New/jhchoi_workdir/jobs//NanoGardening__Autumn18_102X_nAODv5_Full2018v5/NanoGardening__Autumn18_102X_nAODv5_Full2018v5__HMlnjjSel__DYJetsToLL_M-10to50-LO__part0____MCl1loose2018v5__MCCorr2018v5__Semilep2018_whad30.sh
universe = vanilla
output = /cms/ldap_home/jhchoi/HWW_Analysis/slc7/ForDevelopHMlnjjSel2017_New/jhchoi_workdir/jobs//NanoGardening__Autumn18_102X_nAODv5_Full2018v5/NanoGardening__Autumn18_102X_nAODv5_Full2018v5__HMlnjjSel__DYJetsToLL_M-10to50-LO__part0____MCl1loose2018v5__MCCorr2018v5__Semilep2018_whad30.out
error = /cms/ldap_home/jhchoi/HWW_Analysis/slc7/ForDevelopHMlnjjSel2017_New/jhchoi_workdir/jobs//NanoGardening__Autumn18_102X_nAODv5_Full2018v5/NanoGardening__Autumn18_102X_nAODv5_Full2018v5__HMlnjjSel__DYJetsToLL_M-10to50-LO__part0____MCl1loose2018v5__MCCorr2018v5__Semilep2018_whad30.err
log = /cms/ldap_home/jhchoi/HWW_Analysis/slc7/ForDevelopHMlnjjSel2017_New/jhchoi_workdir/jobs//NanoGardening__Autumn18_102X_nAODv5_Full2018v5/NanoGardening__Autumn18_102X_nAODv5_Full2018v5__HMlnjjSel__DYJetsToLL_M-10to50-LO__part0____MCl1loose2018v5__MCCorr2018v5__Semilep2018_whad30.log
accounting_group=group_cms
queue

        '''
	ncpu='8'
        PREPID=self.PREPID
        NEVENT=self.NEVENT
        shname=PREPID+"_"+NEVENT+'.sh'
        outname=PREPID+"_"+NEVENT+'.out'
        errname=PREPID+"_"+NEVENT+'.err'
        logname=PREPID+"_"+NEVENT+'.log'
        ##Need run setup and myrun.sh
        ## exe.sh which runs setup.sh addtime source myrun
        f=open(shname,'w')
        f.write('#! /bin/bash\n')
        f.write('source setup.sh\n')
        f.write('wget --no-check-certificate https://raw.githubusercontent.com/soarnsoar/python_tool/master/add_runtime.py\n')
        f.write("echo 'cmsRun my_cfg.py' > myrun.sh\n")
        f.write('python add_runtime.py myrun.sh\n')
        f.write('source myrun.sh\n')
        os.system('chmod u+x '+shname+'\n')
        f.close()

        f=open('condor_conf.jds','w')
        f.write('executable='+shname+'\n')
        f.write('universe = vanilla\n')
        f.write('requirements = OpSysMajorVer == 6\n')
        f.write('requirements = ( HasSingularity == true )\n')
        f.write('+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el6:latest\n')
        f.write('+SingularityBind = "/cvmfs, /cms, /share"\n')
        
        f.write('output='+outname+'\n')
        f.write('error='+errname+'\n')
        f.write('log='+logname+'\n')
        f.write('transfer_input_files=setup.sh\n')
        f.write('should_transfer_files = YES\n')
        f.write('accounting_group=group_cms\n')
        f.write('request_cpus = '+ncpu+'\n')
	f.write('queue\n')
	f.close()

    def cmsRun(self):##NOT WORKING
        PREPID=self.PREPID
        NEVENT=self.NEVENT
        python_cfg=PREPID+'_1_cfg.py'
        command='cmsRun '+python_cfg+'&> '+PREPID+'_'+NEVENT+'.log'
        #subprocess.call('cmsRun '+python_cfg+'&> '+PREPID+'_'+NEVENT+'.log')
        print "--"+command+"--"
        os.system(command)




        
    def Run(self):
        PREPID=self.PREPID
        NEVENT=self.NEVENT
        
        start = timeit.default_timer()
        mydir=PREPID+"_"+NEVENT
        os.system('mkdir -p '+PREPID+"_"+NEVENT)
        os.chdir(os.getcwd()+'/'+mydir)
        self.get_setup_command()
        self.modify_option('-n',NEVENT)
        self.modify_option('--python_filename','my_cfg.py')
        self.AddCondorJds()
        #self.cmsRun()
        

        #stop = timeit.default_timer()


        #RUNTIME=stop-start


        #SERVER=socket.gethostname()
        #def SendEmail(From,To,Subject,Content):
        #SendEmail('soarnsoar@gmail.com','soarnsoar@gmail.com','FINISHED JOB '+PREPID+"@"+SERVER,'Runtime='+str(RUNTIME)+'\nCURDIR='+os.getcwd()+'\nPREPID='+PREPID+'\nSERVER='+SERVER)


if __name__ == "__main__":
    



    #RunMcM():
    #    def __init__(self,PREPID,NEVENT):
    
    
    parser = argparse.ArgumentParser()
    ####Set options###                                                                                                             
    parser.add_argument("--id", help="PrepID")
    parser.add_argument("--n", help="Nevents")
    
    args = parser.parse_args()

    if args.id:
        PREPID=args.id
    else:
        print "need --id <PrepID>"
        quit()
    if args.n:
        NEVENT=args.n
    else:
        print "need --n <Nevents>"
        quit()


    JOB=RunMcM(PREPID,NEVENT)
    #JOB.run_setup_command()
    JOB.Run()
