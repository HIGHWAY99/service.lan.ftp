# ===================================================================
# --- #
# ===================================================================
import os,sys,re,socket
import xbmcplugin,xbmcaddon,xbmc
try: 			from addon.common.addon 				import Addon
except:
	try: 		from t0mm0.common.addon 				import Addon
	except: 
		try: from c_t0mm0_common_addon 				import Addon
		except: pass
addon_id="service.lan.ftp"
addon_name="FTP [B]HUB[/B][I] - FTP Server[/I]"
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
_artPath		=xbmc.translatePath(os.path.join(addonPath,"art"))
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
def cFL(t,c='blue'): ### For Coloring Text ###
	return '[COLOR '+c+']'+t+'[/COLOR]'
def cFL_(t,c='blue'): ### For Coloring Text ###
	try: return '[COLOR '+c+']'+t[0:1]+'[/COLOR]'+t[1:]
	except: return '[COLOR '+c+']'+t+'[/COLOR]'
isEnabledText="server_enable"
def IsItEnabled(): return tfalse(addst(isEnabledText,"false"))
def ShutDownMenu(): eod(); xbmc.executebuiltin("ActivateWindow(111)"); 
#	#xbmc.executebuiltin('XBMC.ActivateWindow(111)'); 
#	#xbmc.executebuiltin("ActivateWindow(shutdownmenu)"); 
#	###
def art(f,fe=''): return xbmc.translatePath(os.path.join(_artPath,f+fe)) ### for Making path+filename+ext data for Art Images. ###
def artp(f,fe='.png'): return art(f,fe)
def artj(f,fe='.jpg'): return art(f,fe)
def DoE(e): xbmc.executebuiltin(E)
def DoA(a): xbmc.executebuiltin("Action(%s)" % a)
# ===================================================================
# --- Mode Functions
# ===================================================================


def Main(): 
	AddSettingFolder()
	if tfalse(addst("is-serivce-running","false"))==True:
		if tfalse(addst("show-endisserver","false"))==True: 
			addon.add_directory({'mode':'EnableServer'},{'title':cFL_('Enable Server','lime')},is_folder=True,fanart=_artFanart,img=artp("EnableServer"))
			addon.add_directory({'mode':'DisableServer'},{'title':cFL_('Disable Server','red')},is_folder=True,fanart=_artFanart,img=artp("DisableServer"))
		if tfalse(addst("show-serverstatus","false"))==True: ShowTest(); 
		ShowIP(); 
		if tfalse(addst("show-accounts","false"))==True: MenuAccounts(); 
		if tfalse(addst("show-restartxbmc","false"))==True: addon.add_directory({'mode':'ShutDownMenu'},{'title':cFL('Restart XBMC','purple')},is_folder=True,fanart=_artFanart,img=artp("RestartXBMC"))
	else: addon.add_directory({'mode':'ShutDownMenu'},{'title':cFL('Please restart XBMC.','purple')},is_folder=True,fanart=_artFanart,img=artp("RestartXBMC"))
	ShowRefresh()
	DoView(); eod(); 

def ShowRefresh(): addon.add_directory({'mode':'Refresh'},{'title':cFL_('','purple')},is_folder=True,fanart=_artFanart,img=artp('black1'))
def DoView():
	if (tfalse(addst("auto-view","false"))==True): xbmc.executebuiltin("Container.SetViewMode(%s)" % str(addst("default-view","500")))
def MenuAccounts(): 
	if (tfalse(addst("anon-enable","false"))==True):
		anonPath=xbmc.validatePath(xbmc.translatePath(addst("anon-path","special://logpath"))) #.replace(pFindWhat,"|tag|").replace("|tag|",pReplaceWith)
		if (len(anonPath) > 0):
			addon.add_directory({'mode':'System.ExecWait','url':'ftp://'+str(socket.gethostbyname_ex('')[2]).replace("'","").replace('[','').replace(']','')+':'+addst('port','2121')+'/'},{'title':cFL('00.)','darkorange')+' User: '+cFL('[ [I]Anonymous[/I]  ]','darkorange')+'[CR]'+anonPath},is_folder=True,fanart=_artFanart,img=artp("Anonymous"))
	for tn in ['01','02','03','04','05','06','07','08','09','10']:
		if (tfalse(addst(tn+"-enable","false"))==True):
			tt={}; tt['path']=xbmc.validatePath(xbmc.translatePath(addst(tn+"-path","special://logpath")))
			tt['user']=addst(tn+"-user",""); tt['pass']=addst(tn+"-pass","xbmchub"); tt['perm']=addst(tn+"-perm","elradfmwM")
			if (len(tt['user']) > 0) and (len(tt['path']) > 0):
				addon.add_directory({'mode':'GoToFTP','url':tn},{'title':cFL(tn+'.)','darkorange')+' User: '+cFL(tt['user'],'darkorange')+'[CR]'+tt['path']},is_folder=True,fanart=_artFanart,img=artp("User"+tn))
def ShowIP(): 
	if tfalse(addst("show-netsettings","false"))==True: addon.add_directory({'mode':'ShowIP'},{'title':cFL('Local IP[CR]@ Network Settings','darkorange')},is_folder=True,fanart=_artFanart,img=artp("LocalIP"))
	if tfalse(addst("show-ftpurl","false"))==True: addon.add_directory({'mode':'System.ExecWait','url':'ftp://'+str(socket.gethostbyname_ex('')[2]).replace("'","").replace('[','').replace(']','')+':'+addst('port','2121')+'/'},{'title':'ftp://'+cFL(str(socket.gethostbyname_ex('')[2]).replace("'","").replace('[','').replace(']',''),'darkorange')+':'+cFL(addst('port','2121'),'purple')+'/[CR]'+'ftp://'+cFL('[username]','white')+':'+cFL('[password]','white')+'@'+cFL(str(socket.gethostbyname_ex('')[2]).replace("'","").replace('[','').replace(']',''),'darkorange')+':'+cFL(addst('port','2121'),'purple')+'/'},is_folder=True,fanart=_artFanart,img=artp("FTPUrlExample"))
	#addon.add_directory({'mode':'Refresh'},{'title':'ftp://'+cFL(str(socket.gethostbyname_ex('')[2]).replace("'","").replace('[','').replace(']',''),'darkorange')+':'+cFL(addst('port','2121'),'purple')+'/'},is_folder=True,fanart=_artFanart,img=_artIcon)
	#addon.add_directory({'mode':'Refresh'},{'title':'ftp://'+cFL('[username]','white')+':'+cFL('[password]','white')+'@'+cFL(str(socket.gethostbyname_ex('')[2]).replace("'","").replace('[','').replace(']',''),'darkorange')+':'+cFL(addst('port','2121'),'purple')+'/'},is_folder=True,fanart=_artFanart,img=_artIcon)
def AddSettingFolder(): addon.add_directory({'mode':'ShowSettings'},{'title':cFL_('Show Settings','blue')},is_folder=True,fanart=_artFanart,img=artp("ShowSettings"))
def ShowSettingWindow(): 
	print "Showing Addon Settings."; addon.show_settings(); ShowRefresh(); eod(); 
	if (tfalse(addst("auto-back","false"))==True): xbmc.sleep(1000); DoA("Back"); 
def EnableServer(): 
	addstv(isEnabledText,"true"); ShowTest(); DoView(); eod(); 
	if (tfalse(addst("auto-back","false"))==True): xbmc.sleep(1000); DoA("Back"); 
def DisableServer(): 
	addstv(isEnabledText,"false"); ShowTest(); DoView(); eod(); 
	if (tfalse(addst("auto-back","false"))==True): xbmc.sleep(1000); DoA("Back"); 
def ShowTest():
	if IsItEnabled()==True: addon.add_directory({'mode':''},{'title':cFL('Server is enabled','lime')},is_folder=True,fanart=_artFanart,img=artp("ServerIsEnabled"))
	else: addon.add_directory({'mode' :''},{'title':cFL('Server is disabled','red')},is_folder=True,fanart=_artFanart,img=artp("ServerIsDisabled"))
def GoToNetworkSettings(): eod(); xbmc.executebuiltin("ActivateWindow(18)"); 
def ShowAndReturn():
	ShowRefresh(); DoView(); eod(); 
	if (tfalse(addst("auto-back","false"))==True): xbmc.sleep(1000); DoA("Back"); 
def GoToFTP(tn):
	try:
		url='ftp://'+addst(tn+"-user","")+':'+addst(tn+"-pass","xbmchub")+'@'+(str(socket.gethostbyname_ex('')[2]).replace("'","").replace('[','').replace(']',''))+':'+addst('port','2121')+'/'
		xbmc.executebuiltin("XBMC.System.ExecWait(%s)" % url); 
	except: pass
	ShowAndReturn(); 
# ===================================================================
# --- Mode Controls
# ===================================================================
def check_mode(mode='',site='',section='',url=''):
	deb('param >> Mode',mode); 
	#if (mode=='') or (mode=='main') or (mode=='MainMenu') or (__name__=='__main__'): Main(); #ShowSettingWindow(); 
	if (mode=='') or (mode=='main') or (mode=='MainMenu'): Main(); #ShowSettingWindow(); 
	elif (mode=='ShowSettings'): 		ShowSettingWindow(); eod(); #RefreshList()
	elif (mode=='EnableServer'): 		EnableServer(); #RefreshList()
	elif (mode=='DisableServer'): 	DisableServer(); #RefreshList()
	elif (mode=='Refresh'): 				RefreshList()
	elif (mode=='ShutDownMenu'): 		eod(); ShutDownMenu()
	elif (mode=='ShowIP'): 					GoToNetworkSettings()
	elif (mode=='System.Exec'): 		xbmc.executebuiltin("XBMC.System.Exec(%s)" % url); ShowAndReturn(); 
	elif (mode=='System.ExecWait'): xbmc.executebuiltin("XBMC.System.ExecWait(%s)" % url); ShowAndReturn(); 
	elif (mode=='GoToFTP'): 								GoToFTP(url)
	else: Main()
	#
	###
check_mode(addpr('mode',''),addpr('site',''),addpr('section',''),addpr('url',''))