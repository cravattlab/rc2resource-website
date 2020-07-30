from unidecode import unidecode

import pathlib
import csv
import toml
import sys
import click

sys.path.insert(0, '../../../pymed')
import pymed

tool = 'lab_website'
email = 'radus@scripps.edu'


OUTPUT_PATH = pathlib.Path('output')

def query_pubmed(pubmed_ids):
    pubmed = pymed.PubMed(tool=tool, email=email)
    q = pubmed.query(' '.join(map(str, pubmed_ids)) + '[PMID]')

    abbrevs = get_abbrevs()

    result = []

    for article, pubmed_id in zip(q, pubmed_ids):
        pages_el = article.xml.find('.//Pagination/MedlinePgn')
        volume_el = article.xml.find('.//JournalIssue/Volume')
        publication_date = article.publication_date

        year = publication_date.year

        abbrev = abbrevs.get(article.journal, article.journal)
        abbrev = abbrev.rstrip('.').replace('.', '_').replace(' ', '').lower()

        article_info = {
            'title': article.title.rstrip('.'),
            'authors': ', '.join([f"{a['lastname']}, {' '.join(map(lambda x: f'{x}.', a['initials']))}" for a in article.authors]),
            'first_author_last_name': unidecode(article.authors[0]['lastname']),
            'link': f'https://dx.doi.org/{article.doi}',
            'journal': article.journal,
            'volume': volume_el.text if volume_el is not None else '',
            'pages': pages_el.text if pages_el is not None else '',
            'year': year,
            'publish_date': publication_date,
            'image': '',
            'pubmed_id': pubmed_id,
            'doi': article.doi
        }

        result.append(article_info)

    return result


def get_abbrevs():
    filename = 'jrnl_abbrevs.txt'
    num_comment_rows = 3

    with open(filename) as f:
        reader = csv.reader(f, delimiter='\t')
        data = [r for r in reader][num_comment_rows:]

    return dict(data)

@click.command()
@click.argument('ids', nargs=-1)
def main(ids):
    articles = query_pubmed(ids)


    for article in articles:
        print(f'''[[references]]
authors_list = "{article['authors']}"
title = "{article['title']}"
journal = "{article['journal']}"
year = {article['year']}
volume = {article['volume']}
pages = "{article['pages']}"
doi_link = "{article['link']}"
pubmed_link = "https://www.ncbi.nlm.nih.gov/pubmed/{article['pubmed_id']}"'''
    )



if __name__ == '__main__':
    main()
