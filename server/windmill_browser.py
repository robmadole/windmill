#   Copyright (c) 2006 Open Source Applications Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import webbrowser
import os, shutil, subprocess

os.environ['MOZ_NO_REMOTE'] = str(1)
PROXY_HOST = 'localhost'
PROXY_PORT = 4444
DEFAULT_TEST_URL = 'http://www.google.com/windmill-serv/start.html'
MOZILLA_PROFILE_PATH=os.path.abspath("/tmp")
MOZILLA_DEFAUlT_PROFILE=os.path.abspath('/Applications/Firefox.app/Contents/MacOS/defaults/profile/')

class MozillaProfile(object):
    
    def __init__(self, path=MOZILLA_PROFILE_PATH, default_profile=MOZILLA_DEFAUlT_PROFILE,
                  proxy_host=PROXY_HOST, proxy_port=PROXY_PORT, test_url=DEFAULT_TEST_URL):
        """Create profile dir, and populate it"""
        
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.test_url = test_url
        
        self.profile_path = os.path.abspath(path + '/windmill_profile/')
        
        if os.path.exists(self.profile_path) is True:
            shutil.rmtree(self.profile_path)
        
        shutil.copytree(default_profile, self.profile_path)
        
        self.prefs_js_f = open(self.profile_path + '/prefs.js', 'w')
        self.initial_prefs()
    
    def initial_prefs(self):
        """Initial prefs population, separated form __init__ for ease of subclassing"""
        
        # Get rid of default browser check
        self.user_pref('"browser.shell.checkDefaultBrowser", false')
        # Suppress authentication confirmations
        self.user_pref('"network.http.phishy-userpass-length", 255')
        # Disable pop-up blocking
        self.user_pref('"browser.allowpopups", true')
        self.user_pref('"dom.disable_open_during_load", false')
        # Open links in new windows (Firefox 2.0)
        self.user_pref('"browser.link.open_external", 2')
        self.user_pref('"browser.link.open_newwindow", 2')
        # Configure local proxy
        self.user_pref('"network.proxy.http", "%s"' % self.proxy_host)
        self.user_pref('"network.proxy.http_port", %s' % str(self.proxy_port))
        self.user_pref('"network.proxy.type", 1')
        self.user_pref('"startup.homepage_override_url", "' + self.test_url + '"')
        self.user_pref('"browser.startup.homepage", "' + self.test_url + '"')
        self.user_pref('"startup.homepage_welcome_url", ""')
        # Disable security warnings
        self.user_pref('"security.warn_submit_insecure", false')
        self.user_pref('"security.warn_submit_insecure.show_once", false')
        self.user_pref('"security.warn_entering_secure", false')
        self.user_pref('"security.warn_entering_secure.show_once", false')
        self.user_pref('"security.warn_entering_weak", false')
        self.user_pref('"security.warn_entering_weak.show_once", false')
        self.user_pref('"security.warn_leaving_secure", false')
        self.user_pref('"security.warn_leaving_secure.show_once", false')
        self.user_pref('"security.warn_viewing_mixed", false')
        self.user_pref('"security.warn_viewing_mixed.show_once", false')
        # Disable cache
        self.user_pref('"browser.cache.disk.enable", false')
        self.user_pref('"browser.cache.memory.enable", false')
        # Disable "do you want to remember this password?"
        self.user_pref('"signon.rememberSignons", false')
        
        # self.add_js('user_pref("browser.allowpopups", true);')
        # self.add_js('user_pref("browser.cache.disk.enable", false);')
        # self.add_js('user_pref("browser.cache.memory.enable", false);')
        # self.add_js('user_pref("browser.link.open_external", 2);')
        # self.add_js('user_pref("browser.link.open_newwindow", 2);')
        # self.add_js('user_pref("browser.shell.checkDefaultBrowser", false);')
        # self.add_js('user_pref("dom.disable_open_during_load", false);')
        # self.add_js('user_pref("extensions.lastAppVersion", "2.0");')
        # self.add_js('user_pref("network.http.phishy-userpass-length", 255);')
        # self.add_js('user_pref("network.proxy.type", 2);')
        # self.add_js('user_pref("security.warn_entering_secure", false);')
        # self.add_js('user_pref("security.warn_entering_secure.show_once", false);')
        # self.add_js('user_pref("security.warn_entering_weak", false);')
        # self.add_js('user_pref("security.warn_entering_weak.show_once", false);')
        # self.add_js('user_pref("security.warn_leaving_secure", false);')
        # self.add_js('user_pref("security.warn_leaving_secure.show_once", false);')
        # self.add_js('user_pref("security.warn_submit_insecure", false);')
        # self.add_js('user_pref("security.warn_submit_insecure.show_once", false);')
        # self.add_js('user_pref("security.warn_viewing_mixed", false);')
        # self.add_js('user_pref("security.warn_viewing_mixed.show_once", false);')
        # self.add_js('user_pref("signon.rememberSignons", false);')
        
    def user_pref(self, string):
        self.prefs_js_f.write('user_pref(' + string + ');\n')
        self.prefs_js_f.flush()
        
    def add_js(self, string):
        self.prefs_js_f.write(string + '\n')
        self.prefs_js_f.flush()
        
    def clean_up(self):
        shutil.rmtree(self.profile_path)
        
            
MOZILLA_BINARY = '/Applications/Firefox.app/Contents/MacOS/firefox-bin'
        
        
class MozillaBrowser(object):
    """MozillaBrowser class, init requires MozillaProfile instance"""
    def __init__(self, profile, mozilla_bin=MOZILLA_BINARY):

        self.profile = profile
        self.mozilla_bin = mozilla_bin
        self.p_id = None
        
    def open(self, url=None):
        
        if url is None:
            url = self.profile.test_url
        
        self.p_id = subprocess.Popen("%s -profile %s %s" % (self.mozilla_bin, self.profile.profile_path, url), shell=True).pid
        
        print self.mozilla_bin, '-profile %s' % self.profile.profile_path, url
        
    def is_alive(self):
        
        if self.p_id is None:
            return False
        
        try:
            os.kill(self.p_id, 0)
            return True
        except:
            return False
            
    def kill(self, signal=2):
        
        os.kill(self.p_id, signal)
        
if __name__ == "__main__":
    
    print 'Starting Profile'
    profile = MozillaProfile()
    print 'Creating browser obj'
    browser = MozillaBrowser(profile)
    
    print 'Opening default browser'
    browser.open()
    
    print 'Is alive?'
    print browser.is_alive()
    
    import time
    time.sleep(5)
    
    if browser.is_alive():
        print 'killing browser'
        browser.kill()
        if browser.is_alive():
            browser.kill(9)