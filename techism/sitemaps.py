#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from datetime import datetime

class TechismSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return ['/', '/about/']
    
    def location(self, obj):
        return obj

    def lastmod(self, obj):
        return datetime.now()
