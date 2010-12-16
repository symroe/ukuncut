import re

from django.core.management.base import BaseCommand, CommandError

from optparse import make_option

from ukuncut.scrapers.arcadia import scrape as scrape_arcadia
from ukuncut.scrapers.vodafone import scrape as scrape_vodafone
from ukuncut.scrapers.bhs import scrape as scrape_bhs


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--scraper', '-s', dest='scraper',default=None),
        )
    

    def handle(self, *args, **options):
        all_scrapers = ['scrape_bhs', 'scrape_arcadia', 'scrape_vodafone',]
        if not options['scraper']:
            scrapers = all_scrapers
        else:
            scrapers = options.get('scraper').split(',')

        for scraper in scrapers:
            if scraper in all_scrapers:
                globals()[scraper]()
            else:
                for scraper_poss in all_scrapers:
                    if re.search(scraper, scraper_poss):
                        globals()[scraper_poss]()


        # scrape_bhs()
        # scrape_arcadia()
        # scrape_vodafone()
        
