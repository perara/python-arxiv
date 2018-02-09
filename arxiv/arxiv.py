from __future__ import print_function
from .subject import Subject
from .sort import Sort
from .paper import Paper
from .prefix import Prefix
import feedparser

try:
    # Python 2
    from urllib import quote_plus
    from urllib import urlencode
    from urllib import urlretrieve
    from urllib import request
except ImportError:
    # Python 3
    from urllib.parse import quote_plus
    from urllib.parse import urlencode
    from urllib.request import urlretrieve
    from urllib import request


class Arxiv:
    api = 'https://export.arxiv.org/api/'
    Sort = Sort
    Subject = Subject
    Prefix = Prefix

    @staticmethod
    def query(
            prefix=Prefix.all,
            q="",
            id_list=list(),
            start=0,
            max_results=10,
            sort_by=Sort.By.relevance,
            sort_order=Sort.Order.descending):

        url_params = urlencode({"search_query": prefix + ":" + q,
                                "id_list": ','.join(id_list),
                                "start": start,
                                "max_results": max_results,
                                "sortBy": sort_by,
                                "sortOrder": sort_order})

        results = feedparser.parse(Arxiv.api + 'query?' + url_params)
        status_code = results.get('status')

        if status_code == 200:
            return Arxiv._parse_results(results)
        else:
            raise Exception("Could not retrieve response due to HTTP Error (%s)." % status_code)

    @staticmethod
    def _parse_results(results):
        papers = []
        for result in results['entries']:
            paper = Paper.create(result)
            papers.append(paper)
        return papers
