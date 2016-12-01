import sys
def createAuthAlias(aliasName,user,password): 
       print "Creating Auth Alias" 
       security = AdminConfig.getid('/Security:/') 
       alias = ['alias', aliasName] 
       userid = ['userId', user] 
       pw = ['password', password] 
       jaasAttrs = [alias, userid, pw] 
       aliasId = AdminConfig.create('JAASAuthData', security, jaasAttrs) 
       return(aliasId) 

aliasName = sys.argv[0]
user = sys.argv[1]
password = sys.argv[2]
if len(sys.argv[0:]) == 3:
	createAuthAlias(aliasName,user,password)
	AdminConfig.save()
