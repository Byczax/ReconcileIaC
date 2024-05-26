"""
Code inspired from https://github.com/jappeace/distrowatch1graph1svg
"""

import os
import argparse
import json
import re

from requests import Session
from bs4 import BeautifulSoup


def fetch_dist_list_from(baseurl, search_options):
    session = Session()
    website = session.get("%s/search.php?%s" % (baseurl, search_options)).text
    searchSoup = BeautifulSoup(website, "html.parser")

    def tagfilter(tag):
        return tag.name == "b" and re.match("[0-9]+\.", tag.text)

    foundDistributions = searchSoup.find_all(tagfilter)
    print("found %d distributions" % len(foundDistributions))
    return foundDistributions


def fetcher(base_path):
    base_url = "https://distrowatch.com"
    search_options = "ostype=All&category=All&origin=All&basedon=All&notbasedon=None&desktop=All&architecture=All&package=All&rolling=All&isosize=All&netinstall=All&status=All"

    outputdir = "out"
    if not os.path.isdir(outputdir):
        os.mkdir(outputdir)

    fetched_dists_file = f"{base_path}/{outputdir}/dists.json"
    son = ""
    distros = []

    if os.path.isfile(fetched_dists_file):
        with open(fetched_dists_file, "r") as cached:
            print("[MolDiCo] using cached file %s/%s" % (outputdir, fetched_dists_file))
            son = json.loads(cached.read())
            distros = son
    if son == "":
        url = base_url
        print("[MolDiCo] fetching distros from %s" % url)
        son = fetch_dist_list_from(url, search_options)
        for element in son:
            link = element.find("a")
            distros.append(link.text)

        with open(fetched_dists_file, "w") as cached:
            cached.write(json.dumps(distros))

    #! EXCEPTIONS
    distros.append("RHEL")

    return distros
