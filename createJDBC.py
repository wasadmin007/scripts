#Usage: createJDBC.py arg0 arg1  arg2
#  This Script Takes 3 arguments as input
#  Type : Argument1 value is [ Node ] or [ Cluster ] or [ Cell ]
#  Name : Argument2 value is Name of cell or Cluster or cell
# Dict of Jdbc providers
import sys

def save():
   AdminConfig.save()
#
def createJDBC(
scope,
databaseType='DB2',
providerType='"DB2 Universal JDBC Driver Provider"',
implementationType='"XA data source"',
description='"Two-phase commit DB2 JCC provider that supports JDBC 3.0. Data sources that use this provider support the use of XA to perform 2-phase commit processing. Use of driver type 2 on the application server for z/OS is not supported for data sources created under this provider."',
jdbcName='"PraveenTest DB2 Universal JDBC Driver Provider(XA)"',
classpath='[${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc.jar ${UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc_license_cu.jar  ${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc_license_cisuz.jar ]',
nativepath='[${DB2UNIVERSAL_JDBC_DRIVER_NATIVEPATH} ]',
):
        cmd = '[-scope ' + scope
        cmd+= ' -databaseType ' + databaseType
        cmd+= ' -providerType ' + providerType
        cmd+= ' -implementationType ' + implementationType
        cmd+= ' -name ' + jdbcName
        cmd+= ' -description ' + description
        cmd+= ' -classpath ' + classpath
        cmd+= ' -nativePath ' + nativepath +']'
        AdminTask.createJDBCProvider(cmd)
        save()
#

def exist(node,jdbcName) :
 jdbcProviders =  AdminConfig.list('JDBCProvider', AdminConfig.getid('/Cell:'+cell+'/Node:'+node+'/')).split('\r\n')
 for i in  jdbcProviders:
    if  jdbcName.strip( '"' ) in jdbcprovider and node+'|resources.xml#JDBCProvider_' in jdbcprovider:
        return True
    else:
        return False
 #
#

Type = sys.argv[0]
Name = sys.argv[1]
cell = 'cell'
if Type == 'Node' :
    node = Name
    scope = 'Node='+Name
elif Type == 'Cluster' :
    scope = 'Cluster='+Name
elif Type == 'Cell' :
    scope = 'Cell='+Name

dict = {
            'databaseType'   :  'DB2',
            'providerType'   : '"DB2 Universal JDBC Driver Provider"',
            'implementationType'  : '"XA data source"',
            'description' : '"Two-phase commit DB2 JCC provider that supports JDBC 3.0. Data sources that use this provider support the use of XA to perform 2-phase commit processing. Use of driver type 2 on the application server for z/OS is not supported for data sources created under this provider."',
            'jdbcName' : '"PraveenTest DB2 Universal JDBC Driver Provider(XA)"',
            'classpath' : '[${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc.jar ${UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc_license_cu.jar  ${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc_license_cisuz.jar ]',
            'nativepath' : '[${DB2UNIVERSAL_JDBC_DRIVER_NATIVEPATH} ]',
       }

databaseType = dict['databaseType']
providerType = dict['providerType']
implementationType = dict['implementationType']
description = dict['description']
jdbcName = dict['jdbcName']
classpath = dict['classpath']
nativepath = dict['nativepath']
if not exist(node,jdbcName) :
        createJDBC(scope,databaseType=databaseType,providerType=providerType,implementationType=implementationType,description=description,jdbcName=jdbcName,classpath=classpath,nativepath=nativepath)


