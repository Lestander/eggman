################################################################################
#      Copyright (C) 2015 Surfacingx                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import uservar
import time
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from datetime import date, datetime, timedelta
from resources.libs import wizard as wiz

ADDON_ID       = uservar.ADDON_ID
ADDONTITLE     = uservar.ADDONTITLE
ADDON          = wiz.addonId(ADDON_ID)
DIALOG         = xbmcgui.Dialog()
HOME           = xbmc.translatePath('special://home/')
ADDONS         = os.path.join(HOME,      'addons')
USERDATA       = os.path.join(HOME,      'userdata')
PLUGIN         = os.path.join(ADDONS,    ADDON_ID)
PACKAGES       = os.path.join(ADDONS,    'packages')
ADDONDATA      = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADDOND         = os.path.join(USERDATA,  'addon_data')
TRAKTFOLD      = os.path.join(ADDONDATA, 'trakt')
ICON           = os.path.join(PLUGIN,    'icon.png')
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
KEEPTRAKT      = wiz.getS('keeptrakt')
TRAKTSAVE      = wiz.getS('traktlastsave')
COLOR1         = uservar.COLOR1
COLOR2         = uservar.COLOR2
ORDER          = ['placenta','overeasy','poached','scrambled', 'deviled', 'chappaai', 'jor-el', 'neptune', 'yoda', 'legends', 'incursion', 'uranus', 'clickhere', 'reptilia', 'trakt']

TRAKTID = { 
	'placenta': {
		'name'     : 'Placenta',
		'plugin'   : 'plugin.video.placenta',
		'saved'    : 'placenta',
		'path'     : os.path.join(ADDONS, 'plugin.video.placenta'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.placenta', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.placenta', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'placenta_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.placenta', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.placenta/?action=authTrakt)'},
	'overeasy': {
		'name'     : 'Overeasy',
		'plugin'   : 'plugin.video.overeasy',
		'saved'    : 'overeasy',
		'path'     : os.path.join(ADDONS, 'plugin.video.overeasy'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.overeasy', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.overeasy', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'overeasy_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.overeasy', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.overeasy/?action=authTrakt)'},
	'poached': {
		'name'     : 'Poached',
		'plugin'   : 'plugin.video.Poached',
		'saved'    : 'Poached',
		'path'     : os.path.join(ADDONS, 'plugin.video.Poached'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.Poached', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.Poached', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'poached_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.Poached', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.overeasy/?action=authTrakt)'},
	'scrambled': {
		'name'     : 'Scrambled',
		'plugin'   : 'plugin.video.scrambled',
		'saved'    : 'scrambled',
		'path'     : os.path.join(ADDONS, 'plugin.video.scrambled'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.scrambled', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.scrambled', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'scrambled_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.scrambled', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.scrambled/?action=authTrakt)'},
	'deviled': {
		'name'     : 'Deviled',
		'plugin'   : 'plugin.video.deviled',
		'saved'    : 'deviled',
		'path'     : os.path.join(ADDONS, 'plugin.video.deviled'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.deviled', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.deviled', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'deviled_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.deviled', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.deviled/?action=authTrakt)'},
	'chappaai': {
		'name'     : 'Chappaai',
		'plugin'   : 'plugin.video.chappaai',
		'saved'    : 'chappaai',
		'path'     : os.path.join(ADDONS, 'plugin.video.chappaai'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.chappaai', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.chappaai', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'chappaai_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.chappaai', 'settings.xml'),
		'default'  : 'trakt_access_token',
		'data'     : ['trakt_access_token', 'trakt_refresh_token', 'trakt_expires_at'],
		'activate' : 'RunPlugin(plugin://plugin.video.chappaai/authenticate_trakt)'},
	'jor-el': {
		'name'     : 'Jor-El',
		'plugin'   : 'plugin.video.jor-el',
		'saved'    : 'jor-el',
		'path'     : os.path.join(ADDONS, 'plugin.video.jor-el'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.jor-el', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.jor-el', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'jor-el_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.jor-el', 'settings.xml'),
		'default'  : 'trakt_access_token',
		'data'     : ['trakt_access_token', 'trakt_refresh_token', 'trakt_expires_at'],
		'activate' : 'RunPlugin(plugin://plugin.video.jor-el/authenticate_trakt)'},
	'neptune': {
		'name'     : 'Neptune Rising',
		'plugin'   : 'plugin.video.neptune',
		'saved'    : 'neptune',
		'path'     : os.path.join(ADDONS, 'plugin.video.neptune'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.neptune', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.neptune', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'neptune_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.neptune', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.token', 'trakt.refresh'],
		'activate' : 'RunPlugin(plugin://plugin.video.neptune/?action=authTrakt)'},
 'yoda': {
		'name'     : 'Yoda',
		'plugin'   : 'plugin.video.Yoda',
		'saved'    : 'yoda',
		'path'     : os.path.join(ADDONS, 'plugin.video.Yoda'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.Yoda', 'icon.jpg'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.Yoda', 'fanart.png'),
		'file'     : os.path.join(TRAKTFOLD, 'yoda_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.Yoda', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.Yoda/?action=authTrakt)'},
   'legends': {
		'name'     : 'Legends',
		'plugin'   : 'plugin.video.legends',
		'saved'    : 'legends',
		'path'     : os.path.join(ADDONS, 'plugin.video.legends'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.legends', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.legends', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'legends_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.legends', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.legends/?action=authTrakt)'},
	'incursion': {
		'name'     : 'Incursion',
		'plugin'   : 'plugin.video.incursion',
		'saved'    : 'incursion',
		'path'     : os.path.join(ADDONS, 'plugin.video.incursion'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.incursion', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.incursion', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'incursion_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.incursion', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.token', 'trakt.refresh'],
		'activate' : 'RunPlugin(plugin://plugin.video.incursion/?action=authTrakt)'},
 'uranus': {
		'name'     : 'Uranus',
		'plugin'   : 'plugin.video.uranus',
		'saved'    : 'uranus',
		'path'     : os.path.join(ADDONS, 'plugin.video.uranus'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.uranus', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.uranus', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'uranus_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.uranus', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.uranus/?action=authTrakt)'},
 'clickhere': {
		'name'     : 'Clickhere',
		'plugin'   : 'plugin.video.clickhere',
		'saved'    : 'clickhere',
		'path'     : os.path.join(ADDONS, 'plugin.video.clickhere'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.clickhere', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.clickhere', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'clickhere_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.clickhere', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.token', 'trakt.refresh'],
		'activate' : 'RunPlugin(plugin://plugin.video.clickhere/?action=authTrakt)'},
 'reptilia': {
		'name'     : 'Reptilia',
		'plugin'   : 'plugin.video.reptilia',
		'saved'    : 'reptilia',
		'path'     : os.path.join(ADDONS, 'plugin.video.reptilia'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.reptilia', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.reptilia', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'reptilia_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.reptilia', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.reptilia/?action=authTrakt)'},
	'trakt': {
		'name'     : 'Trakt',
		'plugin'   : 'script.trakt',
		'saved'    : 'trakt',
		'path'     : os.path.join(ADDONS, 'script.trakt'),
		'icon'     : os.path.join(ADDONS, 'script.trakt', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'script.trakt', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'trakt_trakt'),
		'settings' : os.path.join(ADDOND, 'script.trakt', 'settings.xml'),
		'default'  : 'user',
		'data'     : ['user', 'Auth_Info', 'authorization'],
		'activate' : 'RunScript(script.trakt, action=auth_info)'}
}

def traktUser(who):
	user=None
	if TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['path']):
			try:
				add = wiz.addonId(TRAKTID[who]['plugin'])
				user = add.getSetting(TRAKTID[who]['default'])
			except:
				return None
	return user

def traktIt(do, who):
	if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
	if not os.path.exists(TRAKTFOLD): os.makedirs(TRAKTFOLD)
	if who == 'all':
		for log in ORDER:
			if os.path.exists(TRAKTID[log]['path']):
				try:
					addonid   = wiz.addonId(TRAKTID[log]['plugin'])
					default   = TRAKTID[log]['default']
					user      = addonid.getSetting(default)
					if user == '' and do == 'update': continue
					updateTrakt(do, log)
				except: pass
			else: wiz.log('[Trakt Info] %s(%s) is not installed' % (TRAKTID[log]['name'],TRAKTID[log]['plugin']), xbmc.LOGERROR)
		wiz.setS('traktlastsave', str(THREEDAYS))
	else:
		if TRAKTID[who]:
			if os.path.exists(TRAKTID[who]['path']):
				updateTrakt(do, who)
		else: wiz.log('[Trakt Info] Invalid Entry: %s' % who, xbmc.LOGERROR)

def clearSaved(who, over=False):
	if who == 'all':
		for trakt in TRAKTID:
			clearSaved(trakt,  True)
	elif TRAKTID[who]:
		file = TRAKTID[who]['file']
		if os.path.exists(file):
			os.remove(file)
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, TRAKTID[who]['name']),'[COLOR %s]Trakt Info: Removed![/COLOR]' % COLOR2, 2000, TRAKTID[who]['icon'])
		wiz.setS(TRAKTID[who]['saved'], '')
	if over == False: wiz.refresh()

def updateTrakt(do, who):
	file      = TRAKTID[who]['file']
	settings  = TRAKTID[who]['settings']
	data      = TRAKTID[who]['data']
	addonid   = wiz.addonId(TRAKTID[who]['plugin'])
	saved     = TRAKTID[who]['saved']
	default   = TRAKTID[who]['default']
	user      = addonid.getSetting(default)
	suser     = wiz.getS(saved)
	name      = TRAKTID[who]['name']
	icon      = TRAKTID[who]['icon']

	if do == 'update':
		if not user == '':
			try:
				with open(file, 'w') as f:
					for trakt in data: 
						f.write('<trakt>\n\t<id>%s</id>\n\t<value>%s</value>\n</trakt>\n' % (trakt, addonid.getSetting(trakt)))
					f.close()
				user = addonid.getSetting(default)
				wiz.setS(saved, user)
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Trakt Info: Saved![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Trakt Info] Unable to Update %s (%s)" % (who, str(e)), xbmc.LOGERROR)
		else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Trakt Info: Not Registered![/COLOR]' % COLOR2, 2000, icon)
	elif do == 'restore':
		if os.path.exists(file):
			f = open(file,mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			match = re.compile('<trakt><id>(.+?)</id><value>(.+?)</value></trakt>').findall(g)
			try:
				if len(match) > 0:
					for trakt, value in match:
						addonid.setSetting(trakt, value)
				user = addonid.getSetting(default)
				wiz.setS(saved, user)
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Trakt: Restored![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Trakt Info] Unable to Restore %s (%s)" % (who, str(e)), xbmc.LOGERROR)
		#else: wiz.LogNotify(name,'Trakt Info: [COLOR red]Not Found![/COLOR]', 2000, icon)
	elif do == 'clearaddon':
		wiz.log('%s SETTINGS: %s' % (name, settings), xbmc.LOGDEBUG)
		if os.path.exists(settings):
			try:
				f = open(settings, "r"); lines = f.readlines(); f.close()
				f = open(settings, "w")
				for line in lines:
					match = wiz.parseDOM(line, 'setting', ret='id')
					if len(match) == 0: f.write(line)
					else:
						if match[0] not in data: f.write(line)
						else: wiz.log('Removing Line: %s' % line, xbmc.LOGNOTICE)
				f.close()
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name),'[COLOR %s]Addon Data: Cleared![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Trakt Info] Unable to Clear Addon %s (%s)" % (who, str(e)), xbmc.LOGERROR)
	wiz.refresh()

def autoUpdate(who):
	if who == 'all':
		for log in TRAKTID:
			if os.path.exists(TRAKTID[log]['path']):
				autoUpdate(log)
	elif TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['path']):
			u  = traktUser(who)
			su = wiz.getS(TRAKTID[who]['saved'])
			n = TRAKTID[who]['name']
			if u == None or u == '': return
			elif su == '': traktIt('update', who)
			elif not u == su:
				if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to save the [COLOR %s]Trakt[/COLOR] data for [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, COLOR1, n), "Addon: [COLOR green][B]%s[/B][/COLOR]" % u, "Saved:[/COLOR] [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]', yeslabel="[B][COLOR %s]Save Trakt[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]No, Cancel[/COLOR][/B]" % COLOR1):
					traktIt('update', who)
			else: traktIt('update', who)

def importlist(who):
	if who == 'all':
		for log in TRAKTID:
			if os.path.exists(TRAKTID[log]['file']):
				importlist(log)
	elif TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['file']):
			d  = TRAKTID[who]['default']
			sa = TRAKTID[who]['saved']
			su = wiz.getS(sa)
			n  = TRAKTID[who]['name']
			f  = open(TRAKTID[who]['file'],mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			m  = re.compile('<trakt><id>%s</id><value>(.+?)</value></trakt>' % d).findall(g)
			if len(m) > 0:
				if not m[0] == su:
					if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to import the [COLOR %s]Trakt[/COLOR] data for [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, COLOR1, n), "File: [COLOR green][B]%s[/B][/COLOR]" % m[0], "Saved:[/COLOR] [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]', yeslabel="[B]Import Trakt[/B]", nolabel="[B]No, Cancel[/B]"):
						wiz.setS(sa, m[0])
						wiz.log('[Import Data] %s: %s' % (who, str(m)), xbmc.LOGNOTICE)
					else: wiz.log('[Import Data] Declined Import(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)
				else: wiz.log('[Import Data] Duplicate Entry(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)
			else: wiz.log('[Import Data] No Match(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)

def activateTrakt(who):
	if TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['path']): 
			act     = TRAKTID[who]['activate']
			addonid = wiz.addonId(TRAKTID[who]['plugin'])
			if act == '': addonid.openSettings()
			else: url = xbmc.executebuiltin(TRAKTID[who]['activate'])
		else: DIALOG.ok("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '%s is not currently installed.' % TRAKTID[who]['name'])
	else: 
		wiz.refresh()
		return
	check = 0
	while traktUser(who) == None:
		if check == 30: break
		check += 1
		time.sleep(10)
	wiz.refresh()