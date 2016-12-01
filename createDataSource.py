import os
import sys
import re
cell = 'Cell01'
def propPrepe(propData):
 info = [ x.strip() for x in propData.read().splitlines() if x ]
 for prop in info :
        key = prop.split('=')[0]
        value = prop.split('=')[1]
        if key == 'DATA_SOURCE_NAME' :
                DATA_SOURCE_NAME = value
                print 'DATA_SOURCE_NAME='+DATA_SOURCE_NAME
                dsName = DATA_SOURCE_NAME
        if key == 'DATA_SOURCE_JNDI_NAME' :
                DATA_SOURCE_JNDI_NAME = value
                print 'DATA_SOURCE_JNDI_NAME='+DATA_SOURCE_JNDI_NAME
                dsJNDI = DATA_SOURCE_JNDI_NAME
        if key == 'DATABASE_USER' :
                DATABASE_USER = value
                print 'DATABASE_USER='+DATABASE_USER
        if key == 'DATABASE_NAME' :
                DATABASE_NAME = value
                print 'DATABASE_NAME='+DATABASE_NAME
                dbName = str(DATABASE_NAME)
        if key == 'DATABASE_PORT' :
                DATABASE_PORT = value
                print 'DATABASE_PORT='+DATABASE_PORT
                dbPort = DATABASE_PORT
        if key == 'DATABASE_SERVER' :
                DATABASE_SERVER = value
                print 'DATABASE_SERVER='+DATABASE_SERVER
                dbHost = DATABASE_SERVER
        if key == 'DATA_SOURCE_PROVIDER' :
                DATA_SOURCE_PROVIDER = value
                print 'DATA_SOURCE_PROVIDER='+DATA_SOURCE_PROVIDER
                jdbcProviderID = DATA_SOURCE_PROVIDER
                if 'there' !=  exist(jdbcProviderID ,dsName):
                        dataSource =  createDataSource(jdbcProviderID ,dsName ,dsJNDI ,  aliasName ,dbtype ,dbName ,dbPort ,dbHost)
                else:
                        print "Data Source Already exist      "
#

def exist(jdbcProviderID,dsName):
	dataSources = AdminConfig.list('DataSource', AdminConfig.getid( '/Cell:'+cell+'/')).split('\n')
        scopeDs = jdbcProviderID.split('|')[0].split('cells')[1]
        pat = dsName+'(cells'+scopeDs+'|resources.xml'
	for dataSource in dataSources:
	  if dataSource != '' :
	     data = dataSource.split('#')[0]
             if data == pat :
        	print dataSource
		return 'there'	 

#
def createDataSource(jdbcProviderID ,dsName ,dsJNDI ,  aliasName ,dbtype ,dbName ,dbPort ,dbHost):
      print "Creating DataSource"
      if dbtype == 'db2' :
                configprops='[[databaseName java.lang.String '+dbName+'] [driverType java.lang.Integer 4] [serverName java.lang.String '+dbHost +'] [portNumber java.lang.Integer '+dbPort+']]'
		ds  = AdminTask.createDatasource(jdbcProviderID, '[-name '+dsName+' -jndiName '+dsJNDI+' -dataStoreHelperClassName com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias '+aliasName+' -xaRecoveryAuthAlias '+aliasName+' -configureResourceProperties '+ configprops+' -description "Testing DataSource"]')
		print ds
		AdminConfig.save()
      elif dbType == 'oracle' :
                ds = AdminTask.createDatasource(jdbcProviderID,'[-name '+dsName+' -jndiName '+dsJNDI+' -dataStoreHelperClassName   com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias '+aliasName+' -xaRecoveryAuthAlias '+aliasName+' -configureResourceProperties [[URL java.lang.String jdbc:oracle:thin:@'+dbHost+':'+dbPort+':'+dbName+']]]')

# Create Data Source Method completion
propFile = sys.argv[0]
if len(sys.argv[0:]) == 1 and os.path.isfile(propFile):
     propData = open( propFile )
     dbtype = 'db2'
     aliasName = ""
     propPrepe(propData) 
elif len(sys.argv[0:])>1 and len(sys.argv[1:])<8:
     DATA_SOURCE_NAME = sys.argv[0]
     DATA_SOURCE_JNDI_NAME = sys.argv[1]
     DATABASE_USER =  sys.argv[2]
     DATABASE_NAME =  sys.argv[3]
     DATABASE_PORT = sys.argv[4]
     DATABASE_SERVER = sys.argv[5]
     DATA_SOURCE_PROVIDER = sys.argv[6]
     dbtype = 'db2'
     aliasName = ""
     dsName = DATA_SOURCE_NAME
     jdbcProviderID = DATA_SOURCE_PROVIDER
     dsJNDI = DATA_SOURCE_JNDI_NAME
     dbName = DATABASE_NAME
     dbPort = DATABASE_PORT
     dbHost = DATABASE_SERVER 
     
     if 'there' != exist(jdbcProviderID ,dsName):
     	     print 'Starting Data Source Creation'
	     dataSource =  createDataSource(jdbcProviderID ,dsName ,dsJNDI ,  aliasName ,dbtype ,dbName ,dbPort ,dbHost)
     else:
          print "Data Source Already exist      "+ dsName
else :
     print 'Usage: script propFile'
     print 'Usage: =====OR ============'
     print 'Usage: DATA_SOURCE_NAME DATA_SOURCE_JNDI_NAME DATABASE_USER DATABASE_NAME DATABASE_PORT DATABASE_SERVER DATA_SOURCE_PROVIDER'
