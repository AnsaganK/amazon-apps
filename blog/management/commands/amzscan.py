from django.core.management.base import BaseCommand
from scanners import main


class Command(BaseCommand):
    help = 'Amazon crawler'

    def handle(self, *args, **options):
        main.run()
