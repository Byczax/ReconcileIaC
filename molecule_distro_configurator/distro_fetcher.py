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


def fetcher():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--baseurl",
        default="https://distrowatch.com",
        help="default http://distrowatch.com",
    )
    parser.add_argument(
        "--searchOptions",
        default="ostype=All&category=All&origin=All&basedon=All"
        + "&notbasedon=None"
        + "&desktop=All&architecture=All&package=All&rolling=All&isosize=All"
        + "&netinstall=All&status=All",
        help="""the GET form generates this at distrowatch.com/search.php
                everything behind the ? can be put in here,
                use this to add constraints to your graph,
                for example if you're only interested in active distro's,
                specify it at the form and copy the resulting GET request in
                this argument""",
    )

    args = parser.parse_args()
    outputdir = "out"
    if not os.path.isdir(outputdir):
        os.mkdir(outputdir)

    fetched_dists_file = outputdir + "/" + "dists.json"
    son = ""
    distros = []
    
    if os.path.isfile(fetched_dists_file):
        with open(fetched_dists_file, "r") as cached:
            print("using cached file %s/%s" % (outputdir, fetched_dists_file))
            son = json.loads(cached.read())
            distros = son
    if son == "":
        url = args.baseurl
        print("fetching distros from %s" % url)
        son = fetch_dist_list_from(url, args.searchOptions)
        for element in son:
            link = element.find("a")
            distros.append(link.text)
            
        with open(fetched_dists_file, "w") as cached:
            cached.write(json.dumps(distros))
            

    return distros
