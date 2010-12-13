from django.core.management.base import BaseCommand, CommandError
from ukuncut.scrapers.arcadia import scrape as scrape_arcadia


class Command(BaseCommand):

    def handle(self, *args, **options):
        scrape_arcadia()