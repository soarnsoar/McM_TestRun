import os
import timeit
from SendEmail import SendEmail
import socket
import subprocess
from urllib2 import urlopen






import argparse
#https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/<PREPID>



class RunMcM():
    def __init__(self,PREPID,NEVENT):
        self.PREPID=PREPID
        self.NEVENT=NEVENT


    def run_setup_command(self):
        PREPID=self.PREPID
        url = 'https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/'+PREPID
        response = urlopen(url).read()

        print '--'+PREPID+'--'
        #f = open('setup.sh', "w")
        #print response
        #f.write(response.strip('"').replace('\\n','\n').strip('\n').strip('"'))
        #f.close()
        os.system('wget '+url)
        os.system('mv '+PREPID+' setup.sh')
        os.system('chmod u+x setup.sh')
        subprocess.call(os.getcwd()+'/setup.sh',shell=True)

    def modify_nevent(self):
        PREPID=self.PREPID
        NEVENT=self.NEVENT
        print "--"+str(NEVENT)+"--"
        f=open('setup.sh','r')
        fnew=open('setup.sh_new','w')

        lines=f.readlines()
        for line in lines:
            if ' -n ' in line:##where defining nevents
                first=line.split(' -n ')[0]
                second=line.split(' -n ')[1]
                second=' '.join(second.split(' ')[1:]) ## remove event value
                newline=first+' -n '+NEVENT+' '+second
                fnew.write(newline)
            else:
                fnew.write(line)
            

        f.close()
        fnew.close()
        os.system('mv setup.sh_new setup.sh')

    def cmsRun(self):
        PREPID=self.PREPID
        NEVENT=self.NEVENT
        python_cfg=PREPID+'_1_cfg.py'
        subprocess.call('cmsRun '+python_cfg+'&> '+PREPID+'_'+NEVENT+'.log',shell=True)
        




        
    def Run(self):
        PREPID=self.PREPID
        NEVENT=self.NEVENT
        
        start = timeit.default_timer()

        os.system('mkdir -p '+PREPID)
        os.chdir(os.getcwd()+'/'+PREPID)
        self.run_setup_command()
        self.modify_nevent()
        self.cmsRun()
        

        stop = timeit.default_timer()


        RUNTIME=stop-start


        SERVER=socket.gethostname()
        #def SendEmail(From,To,Subject,Content):
        SendEmail('soarnsoar@gmail.com','soarnsoar@gmail.com','FINISHED JOB '+PREPID+"@"+SERVER,'Runtime='+str(RUNTIME)+'\nCURDIR='+os.getcwd()+'\nPREPID='+PREPID+'\nSERVER='+SERVER)


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
