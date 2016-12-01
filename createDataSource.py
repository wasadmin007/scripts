import os
import sys
import re
cell = 'cell'
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
                if 'there' != exist(jdbcProviderID ,dsName):
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
elif len(sys.argv[0:])>1 and len(sys.argv[0:])<8:
    args = sys.argv[0:] 
    for arg in args:
      key, value = arg.split('=')
      if 'DATA_SOURCE_NAME' == key : 
           DATA_SOURCE_NAME = value
      if 'DATA_SOURCE_JNDI_NAME' == key:
	   DATA_SOURCE_JNDI_NAME = value
      if 'DATABASE_USER' == key:
	   DATABASE_USER = value
      if 'DATABASE_NAME' == key: 
      	   DATABASE_NAME = value 
      if 'DATABASE_PORT' == key: 
           DATABASE_PORT = value
      if 'DATABASE_SERVER' == key:
	   DATABASE_SERVER = value 
      if 'DATA_SOURCE_PROVIDER' == key :
           DATA_SOURCE_PROVIDER = value
    print DATA_SOURCE_NAME,DATA_SOURCE_JNDI_NAME,DATABASE_USER,DATABASE_NAME,DATABASE_PORT,DATABASE_SERVER,DATA_SOURCE_PROVIDER 
    dbtype = 'db2'
    aliasName = ""
    dsName = DATA_SOURCE_NAME
    jdbcProviderID = DATA_SOURCE_PROVIDER
    dsJNDI = DATA_SOURCE_JNDI_NAME
    dbName = DATABASE_NAME
    dbPort = DATABASE_PORT
    dbHost = DATABASE_SERVER 
    if 'there' != exist(jdbcProviderID ,dsName):
          dataSource =  createDataSource(jdbcProviderID ,dsName ,dsJNDI ,  aliasName ,dbtype ,dbName ,dbPort ,dbHost)
    else:
          print "Data Source Already exist      "
else :
     print 'Usage: scriptName propFile'
     print 'Usage: =====OR ============'
     print 'Usage: DATA_SOURCE_NAME=name DATA_SOURCE_JNDI_NAME= DATABASE_USER= DATABASE_NAME= DATABASE_PORT= DATABASE_SERVER= DATA_SOURCE_PROVIDER='
