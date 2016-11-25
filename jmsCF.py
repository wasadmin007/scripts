
import sys
import os
execfile('/usr/IBM/WebSphere/AppServer/scriptLibraries/resources/JDBC/V70/AdminJDBC.py')

cell='Cell01'
node='AppSrv01'
server='fepocAppServ01'
providerType=''
authAlias='Dmgr01/praveentest'
providerType='DB2 Universal JDBC Driver Provider'
jdbcProvider='"testPraveenJP"'
jndiName='praveen/Test'
myDbName='PRAVEEN'
dbServerName='localhost'
dbPort='50000'
datasourceName='PraveenDS'

getJDBC=AdminConfig.getid('/Cell:'+cell+'/Node:'+node+'/JDBCProvider:'+jdbcProvider+'/')
print getJDBC

#AdminTask.createDatasource(getJDBC, '[-name '+datasourceName+' -jndiName '+jndiName+' -dataStoreHelperClassName com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias '+authAlias+' -xaRecoveryAuthAlias '+authAlias+' -configureResourceProperties [[databaseName java.lang.String '+myDbName+'] [driverType java.lang.Integer 4] [serverName java.lang.String '+dbServerName+'] [portNumber java.lang.Integer '+dbPort+']]]')
newDS=AdminTask.createDatasource(getJDBC, '[-name '+datasourceName+' -jndiName '+jndiName+' -dataStoreHelperClassName com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias '+authAlias+' -xaRecoveryAuthAlias '+authAlias+' -configureResourceProperties [[databaseName java.lang.String '+myDbName+'] [driverType java.lang.Integer 4] [serverName java.lang.String '+dbServerName+'] [portNumber java.lang.Integer '+dbPort+']]]')
print AdminConfig.getid('/Cell:'+cell+'/Node:'+node+'/')
AdminConfig.save()
#print newDS
#print AdminConfig.showAttribute(newDS, 'MappingModule')
#AdminConfig.modify(mapping, [['mappingConfigAlias', ''], ['authDataAlias', authAlias]])
AdminConfig.save()
# Note that scripting list commands may generate more information than is displayed by the administrative console because the console generally filters with respect to scope, templates, and built-in entries.
#AdminConfig.list('DataSource', AdminConfig.getid( '/Cell:Cell01/'))# Note that scripting list commands may generate more information than is displayed by the administrative console because the console generally filters with respect to scope, templates, and built-in entries.
