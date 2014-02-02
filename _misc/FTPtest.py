#!/usr/bin/env python
# $Id: basic_ftpd.py 1174 2013-02-19 11:25:49Z g.rodola $

#  pyftpdlib is released under the MIT license, reproduced below:
#  ======================================================================
#  Copyright (C) 2007-2013 Giampaolo Rodola' <g.rodola@gmail.com>
#
#                         All Rights Reserved
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#  ======================================================================

"""A basic FTP server which uses a DummyAuthorizer for managing 'virtual
users', setting a limit for incoming connections.
"""

import os
import xbmcplugin,xbmcaddon,xbmc
try: 			from addon.common.addon 				import Addon
except:
	try: 		from t0mm0.common.addon 				import Addon
	except: 
		try: from c_t0mm0_common_addon 				import Addon
		except: pass
default_path=xbmc.translatePath("special://home/addons/")
addon_id="service.lan.ftp"
addon_name="FTP Server"
try: 		addon=Addon(addon_id, sys.argv); 
except: 
	try: addon=Addon(addon_id, addon.handle); 
	except: addon=Addon(addon_id, 0); 
plugin=xbmcaddon.Addon(id=addon_id); 
print "%s @ %s" % (addon_name,addon_id)
addonPath	=xbmc.translatePath(plugin.getAddonInfo('path'))
try:		datapath 		=xbmc.translatePath(addon.get_profile()); 
except: datapath 		=""
try: 		_artIcon		=addon.get_icon(); 
except: _artIcon		=""
try: 		_artFanart	=addon.get_fanart()
except: _artFanart	=""
def addstv(id,value=''): addon.addon.setSetting(id=id,value=value) ## Save Settings
def addst(r,s=''): return addon.get_setting(r)   ## Get Settings
def addpr(r,s=''): return addon.queries.get(r,s) ## Get Params
def tfalse(r,d=False): ## Get True / False
	if   (r.lower()=='true' ) or (r.lower()=='t') or (r.lower()=='y') or (r.lower()=='1') or (r.lower()=='yes'): return True
	elif (r.lower()=='false') or (r.lower()=='f') or (r.lower()=='n') or (r.lower()=='0') or (r.lower()=='no'): return False
	else: return d
def eod(): addon.end_of_directory()
def notification(header="", message="", sleep=5000 ): xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i)" % ( header, message, sleep ) )
def myNote(header='',msg='',delay=5000,image='http://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/US_99_%281961%29.svg/40px-US_99_%281961%29.svg.png'): addon.show_small_popup(title=header,msg=msg,delay=delay,image=image)
def isPath(path): return os.path.exists(path)
def isFile(filename): return os.path.isfile(filename)
def get_xbmc_os():
	try: xbmc_os = os.environ.get('OS')
	except: xbmc_os = "unknown"
	return xbmc_os
def get_xbmc_version():
	rev_re = re.compile('r(\d+)')
	try: xbmc_version = xbmc.getInfoLabel('System.BuildVersion')
	except: xbmc_version = 'Unknown'
	return xbmc_version
def log(msg): xbmc.log("### [%s] - %s" % (__scriptname__,msg,),level=xbmc.LOGDEBUG )




from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
#from pyftpdlib.authorizers import WindowsAuthorizer

#def notification(header="", message="", sleep=5000 ): xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i)" % ( header, message, sleep ) )

def ftpstop():
    authorizer=DummyAuthorizer()
    handler=FTPHandler
    handler.authorizer=authorizer
    LiP=addst("address","")
    try: Lport=int(addst("port","2121"))
    except: Lport=2121
    address=(LiP,Lport) #port=2121
    server=FTPServer(address,handler)
    #server.serve_forever()
    notification("FTP Server","Attempting to Close Server...."
    server.close_all()

def ftpstartServer():
    ###
    #addst("password","xbmchub")
    authorizer=DummyAuthorizer()
    if (tfalse(addst("anon-enable","false"))==True):
    	anonPath=xbmc.translatePath(addst("anon-path","special://logpath")).replace("\\","|tag|").replace("|tag|","\\\\")
    	if (len(anonPath) > 0):
    		try: authorizer.add_anonymous(anonPath)
    		except: print"Error adding anonymous user."; pass
    for tn in ['01','02','03','04']:
    	if (tfalse(addst(tn+"-enable","false"))==True):
    		tt={}; tt['path']=xbmc.translatePath(addst(tn+"-path","special://logpath")).replace("\\","|tag|").replace("|tag|","\\\\")
    		tt['user']=addst(tn+"-user","xbmchub")
    		tt['pass']=addst(tn+"-pass","xbmchub")
    		tt['perm']=addst(tn+"-perm","elradfmwM")
    		if (len(tt['user']) > 0) and (len(tt['path']) > 0):
    			try: authorizer.add_user(tt['user'],tt['pass'],tt['path'],perm=tt['perm'])
    			except: print"Error adding user: "+str(tt['user']); pass
    handler=FTPHandler; handler.authorizer=authorizer; handler.banner="pyftpdlib based ftpd ready."
    LiP=addst("address","")
    try: Lport=int(addst("port","2121"))
    except: Lport=2121
    address=(LiP,Lport) #port=2121
    server=FTPServer(address,handler)
    server.max_cons=int(addst("max-connections","5")) #max_connections #256
    server.max_cons_per_ip=int(addst("max-connections-per-ip","5")) #max_connections_per_ip #5
    notification("FTP Server","Starting Server... Port: "+str(Lport))
    server.serve_forever()
    
    
    
    
    
    ###

def ftpstart(path01,user01="user",pass01="xbmchub",perm01='elradfmwM',port=2121,max_connections=5,max_connections_per_ip=5,anonPath=""):
    if len(path01)==0: return
    if len(anonPath)==0: anonPath=path01
    authorizer = DummyAuthorizer()
    #path01=xbmc.translatePath("F:\\zzz__AppData\\XBMC\\portable_data\\addons\\")
    #path01=path01.replace("\\","|tag|").replace("|tag|","\\\\")
    ##path01=path01.replace(os.sep,"|tag|").replace("|tag|","\\\\")
    authorizer.add_anonymous(anonPath)
    authorizer.add_user(user01, pass01, path01, perm=perm01)
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "pyftpdlib based ftpd ready."
    address = ('', port) #port=2121
    server = FTPServer(address, handler)
    server.max_cons = max_connections #256
    server.max_cons_per_ip = max_connections_per_ip #5
    notification("FTP Server","Starting Server....")
    server.serve_forever()

def main():
    ##
    #authorizer = WindowsAuthorizer()
    ## Use Guest user with empty password to handle anonymous sessions.
    ## Guest user must be enabled first, empty password set and profile
    ## directory specified.
    ##authorizer = WindowsAuthorizer(anonymous_user="Guest", anonymous_password="")
    #handler = FTPHandler
    #handler.authorizer = authorizer
    #ftpd = FTPServer(('', 21), handler)
    #ftpd.serve_forever()
    #return
    
    ####################
    
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    #authorizer.add_user('user', '12345', os.getcwd(), perm='elradfmwM')
    #authorizer.add_anonymous(os.getcwd())
    #authorizer.add_user('addons', 'road', os.getcwd(), perm='elradfmwM')
    #authorizer.add_user('addons', 'road', xbmc.translatePath("F:\zzz__AppData\XBMC\portable_data\addons"), perm='elradfmwM')
    #authorizer.add_anonymous(xbmc.translatePath("F:\zzz__AppData\XBMC\portable_data\addons"))
    #path01=xbmc.translatePath("F:\\zzz__AppData\\XBMC\\portable_data\\addons\\")
    path01=xbmc.translatePath("F:\\zzz__AppData\\XBMC\\portable_data\\addons\\")
    path01=path01.replace("\\","|tag|").replace("|tag|","\\\\")
    #path01=path01.replace(os.sep,"|tag|").replace("|tag|","\\\\")
    #authorizer.add_anonymous(path01)
    authorizer.add_user('addons', 'xbmchub', path01, perm='elradfmwM')
    
    

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    #handler.masquerade_address = '151.25.42.11'
    #handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('', 2121)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # start ftp server
    server.serve_forever()

if __name__ == '__main__':
    main()
