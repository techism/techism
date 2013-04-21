#!/usr/local/bin/python
# -*- coding: utf-8 -*-

@require_http_methods(["POST"])
def csp_reporting(request):
	#{
  	#"csp-report": {
    #"document-uri": "http://example.com/signup.html",
    #"referrer": "http://evil.example.net/haxor.html",
    #"blocked-uri": "http://evil.example.net/injected.png",
    #"violated-directive": "img-src *.example.com",
    #"original-policy": "default-src 'self'; img-src 'self' *.example.com; report-uri /_/csp-reports",
  	#}
	#}
	pass


def get_events(request, year, month = None, day = None):
	pass


@require_http_methods(["POST"])
def create(request):
	pass
