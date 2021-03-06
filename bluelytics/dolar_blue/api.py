from django.http import HttpResponse
import json, datetime

from operator import itemgetter
from decimal import Decimal

from dolar_blue.models import DolarBlue, Source
from dolar_blue.utils import DecimalEncoder, arg, mean

def api_dolar(d):
  return {'date': d.date.astimezone(arg).isoformat(),
        'compra': d.value_buy,
        'venta': d.value_sell,
        'name': d.source.source,
        'long_name': d.source.description}

def all_prices():
  all_sources = Source.objects.all()
  allPrices = []
  for src in all_sources:
    if str(src) in ['ambito_financiero', 'oficial', 'invertir_online']:
        today = DolarBlue.objects.filter(source__exact=src).order_by('-date').first()
        dateCalc = today.date.replace(hour=3, minute=0, second=0)
        yesterday = DolarBlue.objects.filter(source__exact=src, date__lt=dateCalc).order_by('-date').first()
        if not yesterday:
          yesterday = today
        ret = {
           'date': today.date.astimezone(arg).isoformat(),
           'compra': today.value_buy,
           'venta': today.value_sell,
           'compra_ayer': yesterday.value_buy,
           'venta_ayer': yesterday.value_sell,
           'name': today.source.source,
           'long_name': today.source.description
           }
        allPrices.append(ret)

        if str(src) == 'oficial':
            allPrices.append(addOficial(ret, 30, 'Dolar Solidario'))

  return allPrices

def avgBlue(input):
  i = 0
  v = 0
  c = 0
  c_a = 0
  v_a = 0
  d = 0
  blue = filter(lambda x: x['name'] in ['ambito_financiero', 'invertir_online'], input)
  return {'date': datetime.datetime.now().isoformat(),
        'compra': mean(map(lambda x: x['compra'], blue)),
        'venta': mean(map(lambda x: x['venta'], blue)),
        'compra_ayer': mean(map(lambda x: x['compra_ayer'], blue)),
        'venta_ayer': mean(map(lambda x: x['venta_ayer'], blue)),
        'name': 'blue',
        'long_name': 'Dolar Blue'
          }

def addOficial(data, perc, newname):
  mult = (100 + perc) / Decimal(100)
  return {
    'date': data['date'],
    'compra': data['compra'] * mult,
    'venta':  data['venta'] * mult,
    'compra_ayer': data['compra_ayer'] * mult,
    'venta_ayer':  data['venta_ayer'] * mult,
    'name': 'oficial_' + str(perc),
    'long_name': newname
    }


def lastprice(request):
  allPrices = all_prices()

  output = []

  output.append(avgBlue(allPrices))

  output+=allPrices

  return HttpResponse(json.dumps(output, cls=DecimalEncoder), mimetype="application/json")
