
import os
import sys

def createCF(CFName, QMName, CFJNDI='jndi/'+CFName, qmgrSvrConnChan):    
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

    AdminTask.createWMQConnectionFactory(Provider, CF_cmd )
# createCF Method Completed

args = sys.argv[0:]
if len(args) >= 3 :
    for arg in args:
        key, value = arg.split('=')
        if  key == 'cell':
            CellScope = value
            Provider = '"WebSphere MQ JMS Provider(cells/'+CellScope+'|resources.xml#builtin_mqprovider)"'
        if  key == 'Cluster':
            ClusScope = value
            Provider = '"WebSphere MQ JMS Provider(cells/'+CellScope+'/clusters/'+ClusScope+'|resources.xml#builtin_mqprovider)"'
        if  key == 'Node':
            NodeScope = value
            Provider = '"WebSphere MQ JMS Provider(cells/'+CellScope+'/nodes/'+Nodescope+'|resources.xml#builtin_mqprovider)"'
        if  key == 'CFName':
            CFName = value
        if  key == 'QMName':
            QMName = value
        if  key == 'CFJNDI':
            CFJNDI = value
        if  key == 'qmgrSvrConnChan':
            qmgrSvrConnChan = value
        if  key == 'qmgrHost':
            qmgrHost = value
        if  key ==  'qmgrPortNumber':
            qmgrPortNumber = value
        if  key == 'ConnNameList':
            ConnNameList = value
        if  key == 'ClChanDefTabURL':
            ClChanDefTabURL = value
    if CFName or QMName or CFJNDI or scope:
        print 'These variables should not be empty script CFName or QMName or CFJNDI or Cell(scope of WebSphere) '
    createCF(CFName, QMName, CFJNDI, qmgrSvrConnChan)
else:    
    print 'Usage: scriptName cell=CellName (Node=name or Cluster=clusterName ) CFName=name  QMName=QM CFJNDI=JNDI qmgrSvrConnChan=CHANNEL.OUT (qmgrHost=HOST qmgrPort=1212 or ConnNameList=CHN1,CH2 or ClChanDefTabURL="http://"'   
        