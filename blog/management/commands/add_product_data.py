from django.core.management.base import BaseCommand
from scanners import get_products_data


class Command(BaseCommand):
    help = 'Collect products data'

    def handle(self, *args, **options):
        get_products_data.run()
