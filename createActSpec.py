import os
import sys
def createCF(ASName, QMName, qmgrSvrConnChan='', CFJNDI=''):    
    if CFJNDI:
        CFJNDI = 'jndi/'+ASName
    if DSCR:
        DSCR = ASName
    if destType:
        destType = 'javax.jms.Queue'
    CF_cmd =  '[-name '+ASName
    CF_cmd+=  ' -jndiName '+ASJNDI
    if qmgrHost != '':
        CF_cmd+=  ' -description '+DSCR
        CF_cmd+=  ' -destinationJndiName '+destJNDI
        CF_cmd+=  ' -destinationType '+destType+' -messageSelector '
        CF_cmd+=  ' -qmgrName '+QMName
        CF_cmd+=  ' -wmqTransportType BINDINGS_THEN_CLIENT -qmgrSvrconnChannel '+qmgrSvrConnChan
        CF_cmd+=  ' -qmgrHostname '+qmgrHost
        CF_cmd+=  ' -qmgrPortNumber '+qmgrPortNumber
        CF_cmd+=  ' ]'
    elif ConnNameList != '':
        CF_cmd+=  ' -description '+DSCR
        CF_cmd+=  ' -destinationJndiName '+destJNDI
        CF_cmd+=  ' -destinationType '+destType+' -messageSelector '
        CF_cmd+=  ' -qmgrName '+QMName
        CF_cmd+=  ' -wmqTransportType BINDINGS_THEN_CLIENT -qmgrSvrconnChannel '+qmgrSvrConnChan
        CF_cmd+=  ' -connectionNameList '+ConnNameList+' ]'
    elif ClChanDefTabURL != '':
        CF_cmd+= ' -description -ccdtUrl '+ClChanDefTabURL
        CF_cmd+= ' -destinationJndiName '+destJNDI
        CF_cmd+= ' -destinationType '+destType+' -messageSelector '
        CF_cmd+= ' -ccdtQmgrName '+QMName+' ]'
    print 'Running Admin Command with params'+Provider,CF_cmd
    CFCMDRUN =  AdminTask.createWMQActivationSpec(Provider, CF_cmd)

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
        if  key.lower == 'asname':
            ASName = value
        if  'desttype' == key.lower:
            destType = value.lower()
            if destType == 'queue':
                destType = 'javax.jms.Queue'
            elif  destType == 'topic':
                destType = 'javax.jms.Topic'
        if 'destjndi' == key.lower:
            destJNDI = value
        if  key.lower == 'qmname':
            QMName = value
        if  key.lower == 'asjndi':
            ASJNDI = value
        if  key.lower == 'qmgrsvrconnchan':
            qmgrSvrConnChan = value
        if  key.lower == 'qmgrhost':
            qmgrHost = value
        if  key.lower ==  'qmgrport':
            qmgrPortNumber = value
        if  key.lower == 'connnamelist':
            ConnNameList = value
        if  key.lower == 'clchandeftaburl':
            ClChanDefTabURL = value
    if ASName or QMName  or CellScope or qmgrHost:
        print CellScope,ClusScope,ASName,QMName,ASJNDI,qmgrHost
        createCF(ASName, QMName ,qmgrSvrConnChan , ASJNDI) 
    else:
        print 'These variables should not be empty script ASName or QMName or ASJNDI or Cell(scope of WebSphere) '
        
else:    
    print 'Usage: scriptName cell=CellName (Node=name or Cluster=clusterName ) ASName=name  QMName=QM ASJNDI=JNDI destJNDI=JNDIdest desttype=queue qmgrSvrConnChan=CHANNEL.OUT (qmgrHost=HOST qmgrPort=1212 or ConnNameList=CHN1,CH2 or ClChanDefTabURL="http://"'   
         