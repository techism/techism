from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, logout
import base64
from functools import wraps

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
            "script-src 'self' *.google-analytics.com;" \
            "img-src 'self' *.google-analytics.com *.tile.openstreetmap.org staticmap.openstreetmap.de *.tiles.mapbox.com;" \
            "style-src 'self' 'unsafe-inline';" \
            "connect-src 'self' nominatim.openstreetmap.org;" \
            "xhr-src 'self' nominatim.openstreetmap.org;" 
        #header for firefox and Internet Explorer 
        response['X-Content-Security-Policy']= standard_policy
        #header for webkit
        response['X-WebKit-CSP']= standard_policy
        #standard header that will be used in future implementations
        response['Content-Security-Policy']= standard_policy
        
        return response


def http_auth(func):
    """
    A decorator, that can be used to authenticate some requests at the site.
    """
    @wraps(func)
    def inner(request, *args, **kwargs):
        result = __http_auth_helper(request)
        if result is not None:
            return result
        return func(request, *args, **kwargs)
    return inner

def __http_auth_helper(request):
    try:
        if not settings.FORCE_HTTP_AUTH:
            # If we don't mind if django's session auth is used, see if the
            # user is already logged in, and use that user.
            if request.user:
                return None
    except AttributeError:
        pass
        
    # At this point, the user is either not logged in, or must log in using
    # http auth.  If they have a header that indicates a login attempt, then
    # use this to try to login.
    if request.META.has_key('HTTP_AUTHORIZATION'):
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == 'basic':
                # Currently, only basic http auth is used.
                words = base64.b64decode(auth[1]).split(':')
                if len(words) == 2:
                    user = authenticate(username=words[0], password=words[1])
                    if user:
                        # If the user successfully logged in, then add/overwrite
                        # the user object of this request.
                        request.user = user
                        return None
    
    # The username/password combo was incorrect, or not provided.
    # Challenge the user for a username/password.
    resp = HttpResponse()
    resp.status_code = 401
    try:
        # If we have a realm in our settings, use this for the challenge.
        realm = settings.HTTP_AUTH_REALM
    except AttributeError:
        realm = ""
    
    resp['WWW-Authenticate'] = 'Basic realm="%s"' % realm
    return resp

