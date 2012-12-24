#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from datetime import datetime


class OrgIndexSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['/orgs/']
    
    def location(self, obj):
        return obj

    def lastmod(self, obj):
        return datetime.now()