import os
import timeit

#ARR_PREPID=[
#HIG-RunIIFall17wmLHEGS-00015,
#]


#https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/<PREPID>



class RunMcM():
    def __init__(self,PREPID,NEVENT):
        self.PREPID=PREPID
        self.NEVENT=NEVENT


    def run_setup_command():

        url = 'https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/'+PREPID
        command = 'wget '+url
        print "--"+command+"--"
        os.system(command)
    def modify_nevent():
        PREPID=self.PREPID
        NEVENT=self.NEVENT
        f=open(PREPID,'r')
        fnew=open(PREPID),'w')

        lines=f.readlines()
        for line in lines:
            if ' -n ' in line:##where defining nevents
                first=line.split(' -n ')[0]
                second=line.split(' -n ')[1]
                second=second.split(' ')[1:] ## remove event value
                newline=first+' -n '+NEVENT+' '+second
                fnew.write(newline)
            else:
                fnew.write(line)


        f.close()
        fnew.close()
    def cmsRun():
        PREPID=self.PREPID
        NEVENT=self.NEVENT
        python_cfg=PREPID+'_1_cfg.py'
        subprocess.call('cmsRun '+python_cfg+'&> '+PERPID+'_'+NEVENT+'.log'+,shell=True)
        




        
    def Run():
        PREPID=self.PREPID
        NEVENT=self.NEVENT
        
        start = timeit.default_timer()


        run_setup_command()
        modify_nevent()
        cmsRun()
        

        stop = timeit.default_timer()


        RUNTIME=stop-start
        
        
