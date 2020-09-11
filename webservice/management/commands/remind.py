from django.core.management.base import BaseCommand, CommandError
from webservice.models.user import User


class Command(BaseCommand):
    help = 'Send mails to those over-timed device-owner.'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        print(User.objects.count())