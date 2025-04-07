import pandas as pd
import numpy as np
import yfinance as yf
from collections import defaultdict

class StockFundamentals:
    def __init__(self, data, ticker):
        self.data = data
        self.ticker = ticker
        self.result = self._go()
        self.raw_data = data['facts']['us-gaap']
        
        # Assign tables as attributes
        self.QuarterlyTable = self.result['QuarterlyTable']
        self.DatedTable = self.result['DatedTable']
        self.MetricStats = self.result['MetricStats']
        self.CombinedTable = self._create_combined_table()
        
    def _go(self):
        # Initialize containers
        self.item_store = defaultdict(list)
        self.metric_stats = []
        self.all_ends = []
        
        # Process JSON data
        self._process_data()
        self.earliestDate = min(self.all_ends) if self.all_ends else pd.Timestamp.now() - pd.DateOffset(years=5)
        self.latestDate = max(self.all_ends) if self.all_ends else pd.Timestamp.now()
        
        # Create tables
        return {
            'QuarterlyTable': self._create_quarterly_table(),
            'DatedTable': self._create_dated_table(),
            'MetricStats': self._create_metric_stats()
        }
    
    def _process_data(self):
        gaap_facts = self.data['facts']['us-gaap']
        
        for key in gaap_facts.keys():
            fact = gaap_facts[key]
            if 'Deprecated' in str(fact.get('label', '')):
                continue
                
            units = fact['units']
            if len(units) != 1:
                continue
                
            unit_key, unit_items = next(iter(units.items()))
            self._process_items(key, unit_key, unit_items)

    def _process_items(self, metric, unit, items):
        valid_items = []
        for item in items:
            if 'frame' in item and 'Q' in item.get('frame', ''):
                end_date = pd.to_datetime(item['end'], format='%Y-%m-%d')
                frame = item['frame'].strip('I').strip('CY')
                
                self.item_store[metric].append({
                    'end': end_date,
                    'value': item.get('val', np.nan),
                    'frame': frame,
                    'unit': unit,
                    'form': item.get('form', '')
                })
                self.all_ends.append(end_date)
                
        if self.item_store[metric]:
            dates = [i['end'] for i in self.item_store[metric]]
            self.metric_stats.append({
                'metric': metric,
                'unit': unit,
                'first_date': min(dates),
                'last_date': max(dates),
                'entry_count': len(dates),
                'forms': ','.join(sorted({i['form'] for i in self.item_store[metric]}))
            })

    def _create_quarterly_table(self):
        quarterly_data = []
        for metric, items in self.item_store.items():
            for item in items:
                try:
                    quarterly_data.append({
                        'quarter': pd.Period(item['frame'], freq='Q'),
                        'metric': metric,
                        'value': item['value']
                    })
                except:
                    continue
                    
        df = pd.DataFrame(quarterly_data)
        return df.pivot_table(
            index='quarter',
            columns='metric',
            values='value',
            aggfunc='first'
        ).sort_index()

    def _create_dated_table(self):
        date_data = []
        for metric, items in self.item_store.items():
            for item in items:
                if '10-Q' in item['form']:
                    date_data.append({
                        'end_date': item['end'],
                        'metric': metric,
                        'value': item['value']
                    })
                    
        df = pd.DataFrame(date_data)
        return df.pivot_table(
            index='end_date',
            columns='metric',
            values='value',
            aggfunc='first'
        ).sort_index()

    def _create_metric_stats(self):
        df = pd.DataFrame(self.metric_stats)
        return df.set_index('metric').sort_values(
            ['entry_count', 'metric'], 
            ascending=[False, True]
        )[['unit', 'first_date', 'last_date', 'entry_count', 'forms']]

    def _create_combined_table(self):
        # Get price data without MultiIndex
        price_data = yf.download(
            self.ticker,
            start=self.earliestDate,
            end=self.latestDate
        )
        
        # Flatten the columns
        price_data.columns = [col[0].lower() for col in price_data.columns.values]
        
        # Merge with DatedTable
        return pd.merge_asof(
            self.DatedTable.sort_index(),
            price_data[['close']].rename(columns={'close': 'price'}),
            left_index=True,
            right_index=True,
            direction='nearest'
        )