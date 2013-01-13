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


#sets the http headers for a Content Security Policy
class ContentSecurityPolicyMiddleware(object):
    
    def process_response(self, request, response):
        
        # exclude CSP for Django Admin and OpenID login
        path = request.get_full_path()
        if path.startswith(('/admin/', '/accounts/login/')):
            return response
        if not 'text/html' in response['Content-Type']:
            return response
        
        standard_policy = "default-src 'self';" \
            "img-src 'self' *.tile.openstreetmap.org staticmap.openstreetmap.de;" \
            "connect-src 'self' nominatim.openstreetmap.org;" \
            "xhr-src 'self' nominatim.openstreetmap.org;" 
        #header for firefox and Internet Explorer 
        response['X-Content-Security-Policy']= standard_policy
        #header for webkit
        response['X-WebKit-CSP']= standard_policy
        #standard header that will be used in future implementations
        response['Content-Security-Policy']= standard_policy
        
        return response
