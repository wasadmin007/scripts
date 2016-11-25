
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys

cellName = AdminConfig.list('Cell')
dsName=sys.argv[0]
userName=sys.argv[1]
password=sys.argv[2]
driverPath=sys.argv[3]
dbHost=sys.argv[4]
dbPort=sys.argv[5]
dbSid=sys.argv[6]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Subs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def createProvider():
      print "Creating JDBC Provider"
      provider = AdminTask.createJDBCProvider('[-scope Cell='+cellName+' 
        -databaseType Oracle -providerType "Oracle JDBC Driver" 
        -implementationType "XA data source" -name "Oracle JDBC Driver (XA)" -description "" 
        -classpath ['+driverPath+'] -nativePath "" ]') 
 return(provider)

def createAuthAlias():
      print "Creating Auth Alias"
      security = AdminConfig.getid('/Security:/')
      alias = ['alias', dsName+'_alias']
      userid = ['userId', userName]
      pw = ['password', password]
      jaasAttrs = [alias, userid, pw]
      aliasId = AdminConfig.create('JAASAuthData', security, jaasAttrs)
      return(aliasId)

def createDataSource(provider, aliasId):
      print "Creating DataSource"
      aliasName =  AdminConfig.showAttribute(aliasId, 'alias') 
      ds = AdminTask.createDatasource(provider, '[-name '+dsName+' -jndiName jdbc/'+dsName+' 
        -dataStoreHelperClassName   com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper 
        -containerManagedPersistence true -componentManagedAuthenticationAlias 
        -xaRecoveryAuthAlias '+aliasName+' 
        -configureResourceProperties [[URL java.lang.String jdbc:oracle:thin:@'+dbHost+':'+dbPort+':'+dbSid+']]]')
      AdminConfig.create('MappingModule', ds, '[[authDataAlias '+aliasName+'] [mappingConfigAlias ""]]')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
provider = createProvider()
aliasId = createAuthAlias()
createDataSource(provider, aliasId)
