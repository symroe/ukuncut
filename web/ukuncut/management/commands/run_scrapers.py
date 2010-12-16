from django.core.management.base import BaseCommand, CommandError
from ukuncut.scrapers.arcadia import scrape as scrape_arcadia
from ukuncut.scrapers.vodafone import scrape as scrape_vodafone
from ukuncut.scrapers.bhs import scrape as scrape_bhs


class Command(BaseCommand):

    def handle(self, *args, **options):
        scrape_bhs()
        scrape_arcadia()
        scrape_vodafone()
        
