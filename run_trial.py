import os
import subprocess as sub
import sys


def prep_in_file(sf,tf,inputs):
    '''
    Opens the scenarop file line-by-line. When a parameter in inputs is
    encountered, the value of the parameter on the next line is changed.
    The 'value_change_flag' is set to one when the value of a parameter
    is to be changed on the next line. Each line is appended to 'out',
    which is saved to the 'code' folder.

    Parameters:
    sf: full path to scenario input file that will act as a template
    tf: full path to trial input file that will be created from sf
    inputs: a dictionary of inputs where the dictionary KEYS are variables
        and the VALUES are the variable values. The first key is 'SCENARIO'
        and the value is the user selected scenario.

    '''
    
    f1 = open(sf,'r')
    value_change_flag=0
    out=''
    for line in f1.readlines():
        if value_change_flag==1:
            line=line.replace(line,str(inputs[parameter_change]))
            out=out+line + '\n'
            value_change_flag=0
        elif value_change_flag==0:
            text=line.split(':')[0]
            if text in inputs.keys():
                value_change_flag=1
                parameter_change=text
                out=out+line
            else:
                out=out+line
    f1.close()
    f2=open(tf,'w')
    f2.write(out)
    f2.close()


def del_trial(d, keep_files):
    '''
    Deletes all files in directory except those with in Keep_files.

    Parameters:
    d: directory
    keep_files: the extentions of files that are not to be deleted.
    '''

    for f in os.listdir(d):
        ext=os.path.splitext(f)[1]
        if ext not in keep_files:
            os.remove('%s/%s' % (d,f))

class main(object):
    '''
    Run ESM trial
    '''
    def __init__(self,scn,v1,v2,v3):
        self.scn = scn
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
    ## Folders, files, and input preperation-------------------------------

    # Code dir: contains this file, child.exe, and temporily stores
    # CHILD model output files
    def run_ESM_trial(self):
        cd=os.path.join(os.path.dirname(sys.argv[0]),'child_code')

        # Scenario dir: contains scenario template input (.in) files
        sd=cd.replace('child_code','scenarios')

        # Prepare model inputs
        # ***code to get inputs from GUI here, outputs the 'inputs' dictionary that's defined on next line
        inputs={'SCENARIO':self.scn,'ST_PMEAN':self.v1,'BLFALL_UPPER':self.v2,'RUNTIME':self.v3}
        scenario=inputs['SCENARIO'].replace(' ','_')
        sf='%s\\%s.in' % (sd,scenario)      # scenario file path
        tf='%s\\trial.in' % cd              # trial file path
        prep_in_file(sf,tf,inputs)          # create tf based upon sf
        ##WG## CLEAN UP PRINT LATER
        print 'Inputs: ', str(inputs), ' sent to model. Starting model.', '\n', str(cd),'\n', os.path.dirname(sys.argv[0])

        ## Run the model-------------------------------------------------------

        print 'Beginning %s...' % scenario

        p = sub.Popen('child trial.in',stdout=sub.PIPE,stderr=sub.PIPE,cwd=cd,shell=True)
        
        ##WG## This code gets the elapsed time (year) of model, used in ESM2.py to determine model progress
        while(True):
          code_running = p.poll() #returns None while subprocess is running
          line = p.stdout.readline()
          try:
              time = line.split('time=')[1].split('.')[0]
              yield time
          except:
              pass
          if(code_running is not None):
            break
        output, errors = p.communicate()

        # Play landscape time-series animation
        # ***For now, the animation will be run after this script is run, manually

        # Wrap-up trial
        ##WG## ADDED .kv, .png FILES TO DO NOT DELETE LIST, UNNECESSARY BUT EXTRA CAUTIOUS
        #del_trial(cd,['.exe','.py','.kv','.png'])
        print 'Complete'