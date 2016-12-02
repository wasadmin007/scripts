import os
import sys
def createQueueDest():
	attbts = '[-name '+queDestName
	attbts+= ' -jndiName '+jndiName
	attbts+= ' -queueName '+queueName
	attbts+= ' -qmgr '+qmgrName
	attbts+= ' -description '+description+' ]'
	crtCMD = AdminTask.createWMQQueue(Provider, attbts)
	AdminConfig.save()
	return crtCMD
#End of CreateQueueDest
description = ''
args = sys.argv[0:]
if len(args) > 3:
     for arg in args:
	key ,value = arg.split('=')
	if 'cell' == key.lower() :
	     cellScope = value
	     Provider = cellScope+'(cells/'+cellScope+'|cell.xml)'
	if 'node' == key.lower(): 	
	     nodeScope = value 
             Provider = nodeScope+'(cells/'+cellScope+'/nodes/'+nodeScope+'|node.xml)'
	if  'cluster' == key.lower():
	     clusterScope == value
	     Provider = clusterScope+'(cells/'+cellScope+'/cluster/'+clusterScope+'|cluster.xml)'    
        if  'quedestname' == key.lower():
 		queDestName  = value
	if 'jndiname' == key.lower():
		jndiName = value
	if 'queuename' == key.lower():
        	queueName = value
	if 'qmgrname'  == key.lower():
 		qmgrName = value
        if 'description' == key.lower():
        	description = value
     if not description :
          description = queueName
     if cellScope or queDestName or jndiName or queueName or qmgrName:
          print createQueueDest()
     else:
	createQue = createQueueDest()
	AdminConfig.save() 
	print 'You must pass following args to the script cellScope and queDestName and jndiName and queueName and qmgrName:'
else:
	print 'Usage scriptNanme (cell=cellname or cell == cellname and node=nodename or cell=cellname and cluster = clustername) quedestname=name jndiname=destJndi queuename=queuename qmgrname=qmgrName (optional description=description )  '
