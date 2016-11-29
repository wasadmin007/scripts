import sys
import re
propFile=sys.argv[0]
propData = open( propFile )
dbtype = 'db2'
aliasName = ""
def exist(jdbcProviderID,dsName):
	dataSources = AdminConfig.list('DataSource', AdminConfig.getid( '/Cell:cell/'))
	scopeDs = jdbcProviderID.split('|')[0].split('cells')[1]
	pat = dsName+'\(cells'+scopeDs+'|resources.xml#DataSource_' 
 	match = re.search(pat, dataSources)
	if match:
		print 'Data Source Already Exist at'+ pat
		return "True"
#	
def createDataSource(jdbcProviderID ,dsName ,dsJNDI ,  aliasName ,dbtype ,dbName ,dbPort ,dbHost):
      print "Creating DataSource"
      if dbtype == 'db2' :
	        configprops='[[databaseName java.lang.String '+dbName+'] [driverType java.lang.Integer 4] [serverName java.lang.String '+dbHost+'] [portNumber java.lang.Integer '+dbPort+']]'	
		ds  = AdminTask.createDatasource(jdbcProviderID, '[-name '+dsName+' -jndiName '+dsJNDI+' -dataStoreHelperClassName com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias '+aliasName+' -xaRecoveryAuthAlias '+aliasName+' -configureResourceProperties '+ configprops+' -description "Testing DataSource"]') 
		if 'jndiName attribute of an existing DataSource object has the same value as' in ds :
				print 'Data Source Already Exist' 
      elif dbType == 'oracle' :
          	ds = AdminTask.createDatasource(jdbcProviderID,'[-name '+dsName+' -jndiName '+dsJNDI+' -dataStoreHelperClassName   com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias '+aliasName+' -xaRecoveryAuthAlias '+aliasName+' -configureResourceProperties [[URL java.lang.String jdbc:oracle:thin:@'+dbHost+':'+dbPort+':'+dbName+']]]')

# Create Data Source Method completion

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
	if not exist(jdbcProviderID ,dsName):
	   dataSource =  createDataSource(jdbcProviderID ,dsName ,dsJNDI ,  aliasName ,dbtype ,dbName ,dbPort ,dbHost)
	else:
	   print "Data Source Already exist      "
