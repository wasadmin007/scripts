import sys
def exist():
	listAuth = AdminTask.listAuthDataEntries().split('\n')
	for list in listAuth:
	   if aliasName == list.split('alias')[1].split(']')[0].strip() :
		return list.split('alias')[1].split(']')[0].strip()
#Exist Method
def createAuthAlias(aliasName,user,password): 
       print "Creating Auth Alias" 
       security = AdminConfig.getid('/Security:/') 
       alias = ['alias', aliasName] 
       userid = ['userId', user] 
       pw = ['password', password] 
       jaasAttrs = [alias, userid, pw] 
       aliasId = AdminConfig.create('JAASAuthData', security, jaasAttrs) 
       print aliasId 

aliasName = sys.argv[0]
user = sys.argv[1]
password = sys.argv[2]
if len(sys.argv[0:]) == 3:
    if aliasName == exist():	
	print 'Autheticaltion Alias with the name'+aliasName+' specified already exist'
    else:
	createAuthAlias(aliasName,user,password)
	AdminConfig.save()
