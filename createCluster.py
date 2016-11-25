
import sys
from org.python.modules import time

"""
-----------------------------------------------------------------

"""
def createCluster (clusterName, modelJVM, nodes, namePrefix, serversPerNode, weight, serverTemplate, transportStartPort, transportInc, wasVersion):
	clusterLogger.traceEnter( [clusterName, modelJVM, nodes, namePrefix, serversPerNode, weight, serverTemplate, transportStartPort, transportInc, wasVersion])

	#---------------------------------------------------------
	# We assume that there is only one cell, and we are on it
	#---------------------------------------------------------
	cellname = AdminControl.getCell()
	cell = AdminConfig.getid("/Cell:"+cellname+"/")

	#---------------------------------------------------------
	# Construct the attribute list to be used in creating a ServerCluster 
	# attribute.	  
	#---------------------------------------------------------

	name_attr = ["name", clusterName]
	desc_attr = ["description", clusterName+" cluster"]
	pref_attr = ["preferLocal", "true"]
	statem_attr = ["stateManagement", [["initialState", "STOP"]]]
	attrs = [name_attr, desc_attr, pref_attr, statem_attr]

	#---------------------------------------------------------
	# Create the server cluster 
	#---------------------------------------------------------

	cluster = AdminConfig.getid("/Cell:"+cellname+"/ServerCluster:"+clusterName)

	if (len(cluster) == 0):
		clusterLogger.info("creating the ServerCluster " + clusterName )
		cluster = AdminConfig.create("ServerCluster", cell, attrs)
	else:
		clusterLogger.info("ServerCluster "+clusterName+" already exists...")
	#endIf 

	#---------------------------------------------------------
	# For each node, create the required number of servers
	# 
	#---------------------------------------------------------
	cloneIndex=1
	for nodeName in nodes.split(","):
		clusterLogger.trace("creating servers on node: " + nodeName)
		node = AdminConfig.getid("/Node:"+nodeName+"/")
	  	if (len(node) == 0):
	  		print "Error: Node not found in WAS Config"
	  		print "The node " + nodeName + " could not be found in the WebSphere configuration"
	  		print "The cluster cannot be created before the managed profiles are created."
	  		print "Please verify that the node exists and has been federated into the cell."
	  		sys.exit(-1)
	  	else:
	  		modelServer  = AdminConfig.getid("/Cell:"+cellname+"/Node:"+nodeName+"/Server:"+modelJVM+"/")
			portIndex = 1  #forStart
			while (portIndex <= int(serversPerNode)):  #forTest
				serverName = namePrefix + str(cloneIndex)
				clusterLogger.trace("processing server: " + serverName + " on node: " + nodeName)
				name_attr = ["memberName", serverName]
				weight_attr = ["weight", weight]
				attrs = [name_attr, weight_attr]
				serverJVM  = AdminConfig.getid("/Cell:"+cellname+"/Node:"+nodeName+"/Server:"+serverName+"/")
				if (len(serverJVM) == 0):
					print "creating server "+ serverName + " on node "+nodeName
					# if serverTemplate is defined then we'll need to grab the containment path for the
					# template we want to use when we create the cluster. If modelServer is also defined
					# then serverTemplate is ignored. You cannot do both.
				 	serverTpl = None
					if (len(serverTemplate) > 0):
						serverTpl = AdminConfig.listTemplates('Server', serverTemplate)
						# fixing a bug whereby listing the template would return the zOS and non zOS serverTpl (we only want non zOS)
						if (serverTemplate == "defaultProcessServer"):
							i=0 
							for tpl in serverTpl.split(newline):
								if (i == 0):
									serverTpl = tpl 
									break
								i=i+1
							#endFor
						#endIf
					#endIf
					clusterLogger.trace("modelServer:" + str(modelServer))
					clusterLogger.trace("serverTpl:" + str(serverTpl))
					if (len(modelServer) > 0):
						print "\t--## Using Model %10s : %10s ##--" % (AdminConfig.showAttribute(modelServer, 'name'), serverName)
						server = AdminConfig.createClusterMember(cluster, node, attrs, modelServer)
					elif (serverTpl != None and len(serverTpl) > 0):
						print "--## Template: " + serverTemplate + " to create " + serverName + " ## --"
						server = AdminConfig.createClusterMember(cluster, node, attrs, serverTpl)
					else:
						print "--## Creating cluster members without Template or Model Server ##--"
						server = AdminConfig.createClusterMember(cluster, node, attrs)
					#endIf
					serverJVM = AdminConfig.getid("/Cell:"+cellname+"/Node:"+nodeName+"/Server:"+serverName+"/")
				else:
					print "cluster: ServerClone "+serverName+" already exists..."
					## make sure the server is part of this cluster already, if it isn't we have a problem
					currentCluster = AdminConfig.showAttribute(serverJVM, "clusterName")
					if (currentCluster != clusterName):
						print "Error: Server " + serverName + " is already a member of cluster " + currentCluster
						print "The cluster member PREFIX property is " + namePrefix
						print "Please verify the PREFIX property in cluster.properties"
						sys.exit(-1)
					#endIf
				#endIf
				WasConfig.updateServerPorts(wasVersion, nodeName, serverName, portIndex, transportInc, transportStartPort)
				portIndex += 1  #forNext
				cloneIndex += 1  #forNext
			#endWhile 
		#endIf - the node id was found and valid
	#endFor

	#---------------------------------------------------------
	# save changes 
	# 
	#---------------------------------------------------------

	print "cluster: saving config changes."
	AdminConfig.save()

	#---------------------------------------------------------
	# Ask the ClusterMgr to refresh its list of clusters 
	# 
	#---------------------------------------------------------

	clusterMgr = AdminControl.completeObjectName("type=ClusterMgr,cell="+cellname+",*")
	if (len(clusterMgr) == 0):
		print "cluster: Error -- clusterMgr MBean not found for cell "+cellname
		return 
	#endIf 
	AdminControl.invoke(clusterMgr, "retrieveClusters")

	# Syncronize the nodes
	AdminHelper.syncCell()

	#---------------------------------------------------------
	# Ask the Cluster MBean to start the cluster
	# 
	#---------------------------------------------------------

	#		print "--## Sleeping 5 seconds ##--"
	#		time.sleep(5)
	
	#		cluster = AdminControl.completeObjectName("type=Cluster,name="+clusterName+",*" )
	#		print "--## Starting Cluster: %20s ##--" % clusterName
	#		AdminControl.invoke(cluster, "start" )

#endDef 

#-----------------------------------------------------------------
# Main
#-----------------------------------------------------------------
#clusterLogger = _Logger("createCluster")

# relies on extra properties
##  -cellProperties configure.properties in CELL scope
##  -properties configure.properties in cluster scope for the new cluster
#optDict, args = SystemUtils.getopt( sys.argv, 'scope:;properties:;nodename:;scopename:;mode:;cellProperties:' )

#propFile=optDict['properties']
#cellFile=optDict['cellProperties']

#cellProps = SystemUtils.getPropertyDict(cellFile)
#properties = SystemUtils.getPropertyDict(propFile)

clusterName = sys.argv[0] 
modelServer = sys.argv[1]
if (not modelServer):
	modelServer = default 
#endIf
nodes = sys.argv[2] 
serverTemplate = str(None)
transportStartPort = 0
transportInc = 0
# remove quotes from nodes property
prefix = sys.argv[3] 
perNode = int(properties["PERNODE"])
weight = sys.argv[4] 
wasVersion = sys.argv[5]
createCluster (clusterName, modelServer, nodes, prefix, perNode, weight, serverTemplate, transportStartPort, transportInc, wasVersion)
# save the config
print "Saving Configuration"
AdminConfig.save()


