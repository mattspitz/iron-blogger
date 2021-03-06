#!/usr/bin/python
from lxml import html
import yaml
import sys
import urllib2
import urlparse

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0'}

with open('bloggers.yml') as f:
    users = yaml.safe_load(f.read())


def fetch_links(url):
    req = urllib2.Request(url, headers=HEADERS)
    tree = html.fromstring(urllib2.urlopen(req).read())
    links = tree.xpath(
        '//link[@rel="alternate"][contains(@type, "rss") or ' +
        'contains(@type, "atom") or contains(@type, "rdf")]')
    candidates = [l for l in links if
                  'atom' in l.attrib['type'] and
                  'comments' not in l.attrib['href'].lower() and
                  'comments' not in l.attrib.get('title','')]
    if candidates:
        return candidates[0].attrib['href']
    elif links:
        return links[0].attrib['href']
    else:
        print >>sys.stderr, "No link found for %s" % (url,)
        return None

for (name, u) in users.items():
    for e in u['links']:
        (title, url) = e[0:2]
        e[0] = e[0].strip()
        if len(e) == 3:
            continue
        link = fetch_links(url)
        if link:
            if not link.startswith('http:'):
                link = urlparse.urljoin(url, link)
            e.append(link)

with open('bloggers.yml', 'w') as f:
    yaml.safe_dump(users, f)
