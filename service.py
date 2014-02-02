# ===================================================================
# --- #
# ===================================================================
import os,sys,re
import xbmcplugin,xbmcaddon,xbmc,logging
try: 			from addon.common.addon 				import Addon
except:
	try: 		from t0mm0.common.addon 				import Addon
	except: 
		try: from c_t0mm0_common_addon 				import Addon
		except: pass
default_path=xbmc.translatePath("special://home/addons/")
addon_id="service.lan.ftp"
addon_name="FTP [B]HUB[/B][I] - FTP Server[/I]"
isEnabledText="server_enable"
try: 		addon=Addon(addon_id,sys.argv); 
except: 
	try: addon=Addon(addon_id,addon.handle); 
	except: addon=Addon(addon_id,0); 
plugin=xbmcaddon.Addon(id=addon_id); 
print "%s @ %s" % (addon_name,addon_id)
addonPath=xbmc.translatePath(plugin.getAddonInfo('path'))
try:		datapath 		=xbmc.translatePath(addon.get_profile()); 
except: datapath 		=""
try: 		_artIcon		=addon.get_icon(); 
except: _artIcon		=""
try: 		_artFanart	=addon.get_fanart()
except: _artFanart	=""
#_artMessage=xbmc.translatePath(os.path.join(addonPath,"msg.png"))
# ===================================================================
# --- Common Functions
# ===================================================================
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
def IsItEnabled(): return tfalse(addst(isEnabledText,"false"))
# ===================================================================
# --- Service
# ===================================================================
addstv("is-serivce-running","true")
STARTUP=True; ClosedYet=False; ClosedYetError=False; 
from pyftpdlib.authorizers import DummyAuthorizer; from pyftpdlib.handlers import FTPHandler; from pyftpdlib.servers import FTPServer; 
authorizer=DummyAuthorizer()
ENABLED=IsItEnabled()
if (ENABLED==False):
	while (ENABLED==False): ENABLED=IsItEnabled(); #xbmc.sleep(5000)
while (not xbmc.abortRequested): #while (ENABLED==True) and (not xbmc.abortRequested):
	ENABLED=IsItEnabled(); #print "---" ;print ENABLED
	if (ENABLED==False) and (ClosedYetError==False) and (ClosedYet==False) and (STARTUP==False):
		print "isEnabled="+str(ENABLED)
		print "Attempting to Close Server...."; notification("FTP Server","Attempting to Close Server....")
		STARTUP=True; 
		try: server.serve_forever(timeout=1,blocking=False)
		except: pass
		xbmc.sleep(1000)
		try: server.ip_map=[]; print "did: server.ip_map=[]"; 
		except: print "failed: server.ip_map=[]"; pass
		try: server.socket.close(); print "did: server.socket.close()"; 
		except: print "failed: server.socket.close()"; pass
		try: server.close_all(); print "did: server.close_all()"; ClosedYet=True
		except: ClosedYetError=True; pass
	if (STARTUP==True) and (ENABLED==True):
		STARTUP=False; print "Startup"; pFindWhat="\\"; pReplaceWith="\\\\"
		if (tfalse(addst("anon-enable","false"))==True):
			anonPath=xbmc.validatePath(xbmc.translatePath(addst("anon-path","special://logpath"))) #.replace(pFindWhat,"|tag|").replace("|tag|",pReplaceWith)
			if (len(anonPath) > 0):
				print "user : "+"[anonymous]"+" : path :"+str(anonPath)+" :"
				try: authorizer.add_anonymous(anonPath)
				except: print"Error adding anonymous user."; pass
		for tn in ['01','02','03','04','05','06','07','08','09','10']:
			if (tfalse(addst(tn+"-enable","false"))==True):
				tt={}; tt['path']=xbmc.validatePath(xbmc.translatePath(addst(tn+"-path","special://logpath"))) #.replace(pFindWhat,"|tag|").replace("|tag|",pReplaceWith)
				tt['user']=addst(tn+"-user",""); tt['pass']=addst(tn+"-pass","xbmchub"); tt['perm']=addst(tn+"-perm","elradfmwM")
				if (len(tt['user']) > 0) and (len(tt['path']) > 0):
					print "user : "+str(tt['user'])+" : path :"+str(tt['path'])+" :"
					try: authorizer.add_user(tt['user'],tt['pass'],tt['path'],perm=tt['perm'])
					except: print"Error adding user: "+str(tt['user']); pass
		handler=FTPHandler; handler.authorizer=authorizer; handler.banner="pyftpdlib based ftpd ready."
		try: LiP=addst("address","")
		except: LiP=""
		try: Lport=int(addst("port","2121"))
		except: Lport=2121
		address=(LiP,Lport); server=FTPServer(address,handler); server.max_cons=int(addst("max-connections","5")); server.max_cons_per_ip=int(addst("max-connections-per-ip","5")); 
		print "Starting Server... Port: "+str(Lport); notification("FTP Server","Starting Server... Port: "+str(Lport))
		#server.serve_forever()
		try: server.serve_forever(timeout=int(addst("timeout","10")),blocking=False)
		except: pass
	elif (STARTUP==False) and (ENABLED==True):
		try: server.serve_forever(timeout=int(addst("timeout","10")),blocking=False)
		except: pass
print "Service While Loop has been exited."; print "isEnabled="+str(ENABLED); print "Attempting to Close Server...."; notification("FTP Server","Attempting to Close Server....")
addstv("is-serivce-running","false")
try: server.ip_map=[]
except: print "failed: server.ip_map=[]"; pass
try: server.socket.close()
except: print "failed: server.socket.close()"; pass
try: server.close_all()
except: pass
sys.exit()
