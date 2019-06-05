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


    def get_setup_command(self):
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
