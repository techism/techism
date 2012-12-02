from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import logout

class SecureRequiredMiddleware(object):
    
    def __init__(self):
        self.paths = settings.HTTPS_PATHS
        self.enabled = self.paths and len(self.paths) > 0
    
    def process_request(self, request):
        if not self.enabled:
            return None
        
        if request.is_secure():
            return None
        
        # destroy session if session cookie was submitted over non-secure connection
        if request.user.is_authenticated():
            logout(request)
            return HttpResponseRedirect('/')
            
        # redirect HTTPS_PATHS to HTTPS_URL
        path = request.get_full_path()
        if path.startswith(self.paths):
            secure_url = settings.HTTPS_URL + request.get_full_path()
            return HttpResponseRedirect(secure_url)
