import csv
import os
import argparse

from django.core.management.base import BaseCommand
from core.models import Currency, CurrencyExchangeRate


class Command(BaseCommand):
    """Django command to insert mock data in db"""

    def add_arguments(self, parser):
        parser.add_argument(
            "-p", "--path",
            dest="input_path", help="Input path to load exchanges rates", type=str, default='data/')

    def _insert_data(self, file_path, model):
        # currency_csv = csv.reader(currency_file)
        self.stdout.write('Inserting csv data in db ...')
        with open(file_path) as f:
            csv_reader = csv.DictReader(f, delimiter=',')
            for raw in csv_reader:
                if model == Currency:
                    model.objects.create(
                        code=raw['code'],
                        name=raw['name'],
                        symbol=raw['symbol']

                    )
                if model == CurrencyExchangeRate:
                    model.objects.create(
                        source_currency=Currency.objects.get(code=raw['source_currency']),
                        exchanged_currency=Currency.objects.get(code=raw['exchanged_currency']),
                        valuation_date=raw['valuation_date'],
                        rate_value=raw['rate_value']

                    )
        self.stdout.write('Finished inserting csv data in db!!!')

    def _clean_data(self):
        self.stdout.write('Cleaning data in db ...')
        Currency.objects.all().delete()
        CurrencyExchangeRate.objects.all().delete()


    def handle(self, *args, **options):
        input_path = options.get('input_path')
        currency_file = f"{input_path}/mock_currency.csv"
        rates_file = f"{input_path}/mock_rates.csv"
        self._clean_data()
        self._insert_data(currency_file, Currency)
        self._insert_data(rates_file, CurrencyExchangeRate)







