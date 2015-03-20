# -*- coding: utf-8 -*-
import os
import codecs
import sys
import urllib
import json

from wekeypedia.wikipedia_page import WikipediaPage as Page, url2title, url2lang
from wekeypedia.wikipedia_network import WikipediaNetwork
from wekeypedia.exporter.nx_json import NetworkxJson

from multiprocessing.dummy import Pool as ThreadPool

specialization = json.load(codecs.open("data/wikipedia-geometry/specialization.json","r", "utf-8-sig"))

def fetch_page(source):
  print "📄  fetching: %s" % source.encode('utf-8-sig')

  p = Page()
  r = p.fetch_from_api_title(source.strip(), { "redirects":"true", "rvparse" : "true", "prop": "info|revisions", "inprop": "url", "rvprop": "content" })

  with codecs.open("data/wikipedia-geometry/pages/%s.json" % (source), "w", "utf-8-sig") as f:
    json.dump(r, f)

def fetch_revisions(source):
  print "📄  fetching revisions: %s" % source.encode('utf-8-sig')

  p = Page()
  p.fetch_from_api_title(source.strip())
  r = p.get_all_editors()

  with codecs.open("data/wikipedia-geometry/revisions/%s.json" % (source), "w", "utf-8-sig") as f:
    json.dump(r, f)  

pool = ThreadPool(8)

for p in specialization:
  # fetch_page(p["pagename"])
  # fetch_revisions(p["pagename"])

  pool.apply_async(fetch_page, args=(p["pagename"],))
  pool.apply_async(fetch_revisions, args=(p["pagename"],))

pool.close()
pool.join()

