import concurrent.futures
import httpx
import logging
import os
import random
import re
import sys
import threading
import yaml

from bs4 import BeautifulSoup

logger = logging.getLogger('randcrawler')

def parse_cfg(cfg_file):
    cfg = None
    if os.path.exists(cfg_file): 
        try:
            with open(cfg_file, 'r') as f:
                cfg = yaml.safe_load(f)
        except Exception as e:  # pragma: no cover
            logger.error('Configuration could not be loaded.')
            logger.error(
                    'Failed to load config with error: {0}'.format(str(e)))
    else:
        logger.error('Configuration could not be found.')

    return cfg

def get_sites(site_file):
    sites = []
    if os.path.exists(site_file): 
        try:
            with open(site_file, 'r') as f:
                sites = f.read().splitlines()
        except Exception as e:  # pragma: no cover
            logger.error('Site list could not be loaded.')
            logger.error(
                    'Failed to load site list with error: {0}'.format(str(e)))
    else:
        logger.error('Site list could not be found.')

    return sites

def browse(sites, cfg_max_depth):
    site = sites[random.randint(0,len(sites)-1)]
    if not site.startswith('http://'):
        site = 'http://' +  site

    max_depth = random.randint(1, cfg_max_depth)
    crawl(site, 0, max_depth)

def crawl(url, depth, max_depth):
    print(f'visting {url}')
    req = httpx.get(url)

    if depth <= max_depth:
        soup = BeautifulSoup(req.text, "html5lib")
        links = []
        for h in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            links.append(h.get('href'))
        if len(links) > 0:
            to_follow = links[random.randint(0,len(links)-1)]
            crawl(to_follow, depth + 1, max_depth)   

if __name__ == '__main__':  # pragma: no cover
    cfg = parse_cfg('./crawlercfg.yaml')
    sites = get_sites('./valid_sites.txt')

    cfg_max_concurrent = cfg['max_concurrent'] if cfg['max_concurrent'] else 1
    cfg_max_depth = cfg['max_depth'] if cfg['max_depth'] else 1

    try:
        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=cfg_max_concurrent) as executor:
            while True:
                if len(futures) < cfg_max_concurrent:
                    executor.submit(browse, sites, cfg_max_depth)

                for f in futures:
                    if f.done():
                        futures.remove(f)
    except KeyboardInterrupt:
        print(f'CTRL-C received. Stopping..................................')
        sys.exit()