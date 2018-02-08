import json
import time
try:
    # Python 2
    from urllib import urlretrieve
except ImportError:
    # Python 3
    from urllib.request import urlretrieve


class Paper:

    def __init__(self,
                 title,
                 summary,
                 published,
                 updated,
                 page_url,
                 pdf_url,
                 category,
                 doi,
                 journal,
                 comment,
                 authors,
                 affiliation
                 ):
        self.title = title
        self.summary = summary
        self.authors = authors
        self.comment = comment
        self.affiliation = affiliation
        self.page_url = page_url
        self.pdf_url = pdf_url
        self.doi = doi
        self.journal = journal
        self.updated = updated
        self.published = published
        self.category = category

    def __str__(self):
        return json.dumps({
            'title': self.title,
            'summary': self.summary,
            'comment': self.comment,
            'affiliation': self.affiliation,
            'page_url': self.page_url,
            'pdf_url': self.pdf_url,
            'doi': self.doi,
            'journal': self.journal,
            'updated': time.strftime('%Y-%m-%dT%H:%M:%SZ', self.updated),
            'published': time.strftime('%Y-%m-%dT%H:%M:%SZ', self.published),
            'category': self.category
        })

    def _get_id(self):
        return self.page_url.split("/")[-1]

    def download(self, dirname='./', prepend_id=False, short_name=False):

        if self.pdf_url is None or self.title is None:
            return False

        filename = Paper._get_filename(self.title) if short_name else self.title
        filename = filename + self._get_id() if prepend_id else filename
        filename = dirname + filename + ".pdf"
        urlretrieve(self.pdf_url, filename)

    @staticmethod
    def _get_filename(title):
        filename = ''.join(c if c.isalnum() else '_' for c in title)
        filename = '_'.join(list(filter(None, filename.split('_'))))
        return filename

    @staticmethod
    def create(item):

        title = item['title'].replace("\n", "")
        updated = item['updated_parsed']
        published = item['published_parsed']
        summary = item['summary']
        authors = [author['name'] for author in item['authors']]
        comment = item['arxiv_comment'] if 'arxiv_comment' in item else ''
        page_url = item['link'].replace('http', 'https')
        pdf_url = [t['href'] for t in item['links'] if 'pdf' in t['type']]
        pdf_url = pdf_url[0] if len(pdf_url) > 0 else None
        category = item['arxiv_primary_category']['term']
        affiliation = item.pop('arxiv_affiliation', '')
        journal = item.pop('arxiv_journal_ref', '')
        doi = item.pop('arxiv_doi', '')

        return Paper(
            title=title,
            summary=summary,
            published=published,
            updated=updated,
            page_url=page_url,
            pdf_url=pdf_url,
            category=category,
            doi=doi,
            journal=journal,
            comment=comment,
            authors=authors,
            affiliation=affiliation
        )
