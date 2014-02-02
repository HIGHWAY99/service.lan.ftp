# ===================================================================
# --- #
# ===================================================================
import os,sys,re
import xbmcplugin,xbmcaddon,xbmc
try: 			from addon.common.addon 				import Addon
except:
	try: 		from t0mm0.common.addon 				import Addon
	except: 
		try: from c_t0mm0_common_addon 				import Addon
		except: pass
addon_id="service.lan.ftp"
addon_name="FTP Server"
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
_artMessage=xbmc.translatePath(os.path.join(addonPath,"msg.png"))
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
def RefreshList(): xbmc.executebuiltin("XBMC.Container.Refresh")
def log(msg): xbmc.log("### [%s] - %s" % (__scriptname__,msg,),level=xbmc.LOGDEBUG )
_debugging=True
def WhereAmI(t): ### for Writing Location Data to log file ###
	if (_debugging==True): print 'Where am I:  '+t
def deb(s,t): ### for Writing Debug Data to log file ###
	if (_debugging==True): print s+':  '+t
def debob(t): ### for Writing Debug Object to log file ###
	if (_debugging==True): print t

# ===================================================================
# --- Mode Functions
# ===================================================================


def Main(): eod()


def ShowSettingWindow(): print "Showing Addon Settings."; addon.show_settings(); 



# ===================================================================
# --- Mode Controls
# ===================================================================
def check_mode(mode='',site='',section='',url=''):
	deb('param >> Mode',mode); 
	if (mode=='') or (mode=='main') or (mode=='MainMenu') or (__name__=='__main__'): Main(); ShowSettingWindow(); 
	#
	###
check_mode(addpr('mode',''),addpr('site',''),addpr('section',''),addpr('url',''))