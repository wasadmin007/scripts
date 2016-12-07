import os
import sys
#Usage
#/usr/WebSphere8/AppServer/profiles/dmgr/bin/wsadmin.sh -lang jython -user femadmin -password 27f3m13 -f createCFC.py cell=cell Cluster=cluster1 CFName=sdfs QMName=abc CFJNDI=sfsd qmgrHost=feprafd1 qmgrPort=1414
def createCF(CFName, QMName, qmgrSvrConnChan='', CFJNDI=''):    
    if CFJNDI:
        CFJNDI = 'jndi/'+CFName
    CF_cmd =  '[-type CF -name '+CFName
    CF_cmd+=  ' -jndiName '+CFJNDI
    if qmgrHost != '':
        CF_cmd+=  ' -description -qmgrName '+QMName
        CF_cmd+=  ' -wmqTransportType BINDINGS_THEN_CLIENT -qmgrSvrconnChannel '+qmgrSvrConnChan
        CF_cmd+=  ' -qmgrHostname '+qmgrHost
        CF_cmd+=  ' -qmgrPortNumber '+qmgrPortNumber
        CF_cmd+=  ' ]'
    elif ConnNameList != '':
        CF_cmd+=  ' -description -qmgrName '+QMName
        CF_cmd+=  ' -wmqTransportType BINDINGS_THEN_CLIENT -qmgrSvrconnChannel '+qmgrSvrConnChan
        CF_cmd+=   ' -connectionNameList '+ConnNameList+' ]'
    elif ClChanDefTabURL != '':
        CF_cmd+= ' -description -ccdtUrl '+ClChanDefTabURL+' -ccdtQmgrName '+QMName+' ]'
    print 'Running Admin Command with params'+Provider,CF_cmd
    CFCMDRUN = AdminTask.createWMQConnectionFactory(Provider, CF_cmd )
    AdminConfig.save()
    # createCF Method Completed
qmgrSvrConnChan = ''
qmgrHost=''
ConnNameList=''
ClChanDefTabURL=''


args = sys.argv[0:]
if len(args) >= 4 :
    for arg in args:
        key, value = arg.split('=')
        if  key.lower == 'cell':
            CellScope = value
            Provider = '"WebSphere MQ JMS Provider(cells/'+CellScope+'|resources.xml#builtin_mqprovider)"'
        if  key.lower == 'cluster':
            ClusScope = value
            Provider = '"WebSphere MQ JMS Provider(cells/'+CellScope+'/clusters/'+ClusScope+'|resources.xml#builtin_mqprovider)"'
        if  key.lower == 'node':
            NodeScope = value
            Provider = '"WebSphere MQ JMS Provider(cells/'+CellScope+'/nodes/'+Nodescope+'|resources.xml#builtin_mqprovider)"'
        if  key.lower == 'cfName':
            CFName = value
        if  key.lower == 'qmname':
            QMName = value
        if  key.lower == 'cfjndi':
            CFJNDI = value
        if  key.lower == 'qmgrsvrconnchan':
            qmgrsvrconnchan = value
        if  key.lower == 'qmgrhost':
            qmgrHost = value
        if  key.lower ==  'qmgrport':
            qmgrPortNumber = value
        if  key.lower == 'connnamelist':
            ConnNameList = value
        if  key.lower == 'clchandeftaburl':
            ClChanDefTabURL = value
    if CFName or QMName  or CellScope or qmgrHost:
        print CellScope,ClusScope,CFName,QMName,CFJNDI,qmgrHost
        createCF(CFName, QMName ,qmgrSvrConnChan , CFJNDI) 
    else:
        print 'These variables should not be empty script CFName or QMName or CFJNDI or Cell(scope of WebSphere) '
        
else:    
    print 'Usage: scriptName cell=CellName (Node=name or Cluster=clusterName ) CFName=name  QMName=QM CFJNDI=JNDI qmgrSvrConnChan=CHANNEL.OUT (qmgrHost=HOST qmgrPort=1212 or ConnNameList=CHN1,CH2 or ClChanDefTabURL="http://"'   
        