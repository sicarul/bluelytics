from django.core.management.base import BaseCommand, CommandError
from dolar_blue.models import DolarBlue, Source, Currency, CurrencyValue
from django.utils import timezone

from decimal import Decimal
import sys, datetime, json
from dolar_blue.utils import DecimalEncoder, arg


def maxCurrencies():
  all_currencies = Currency.objects.all()
  maxCurrencies = []
  for cur in all_currencies:
    record = CurrencyValue.objects.filter(curr__exact=cur).order_by('-date').first()
    maxCurrencies.append(record)

  return maxCurrencies

class Command(BaseCommand):
    args = 'file'
    help = 'Exports currencies'


    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Incorrect arguments')
        try:
            output = maxCurrencies()

            with open(args[0], 'w') as j:
                json.dump(output, j, cls=DecimalEncoder)

            self.stdout.write('Successfully exported currency data')
        except Exception:
            self.stdout.write('Error exporting currency data')
            print "Error:", sys.exc_info()[0]
            raise
