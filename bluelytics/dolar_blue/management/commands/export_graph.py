from django.core.management.base import BaseCommand, CommandError
from dolar_blue.models import DolarBlue, Source
from django.utils import timezone

from decimal import Decimal
import sys, datetime, json
from dolar_blue.utils import DecimalEncoder, arg
from django.db import connection

def last_prices_each_day():
    cursor = connection.cursor()
    cursor.execute("""
        select
          case when db.source_id = 'oficial' then 'Oficial' else 'Blue' end as source_id, date(db.date) as date, median(db.value_buy) as value_buy, median(db.value_sell) as value_sell
          from
          dolar_blue_dolarblue db
          group by 1, 2
          order by date desc
    """)

    return cursor.fetchall()

def api_mini_dolar(d):
    return {
    'source': d[0],
    'date': d[1],
    'value': d[3] #value_sell
    }

class Command(BaseCommand):
    args = 'valor_compra valor_venta'
    help = 'Adds the specified dollar value to the database'


    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Incorrect arguments')
        print args
        try:
            output = map(api_mini_dolar, last_prices_each_day())

            with open(args[0], 'w') as j:
                json.dump(output, j, cls=DecimalEncoder)

            self.stdout.write('Successfully exported graph data')
        except Exception:
            self.stdout.write('Error exporting graph data')
            print "Error:", sys.exc_info()[0]
            raise
