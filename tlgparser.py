# -*- coding: utf-8 -*-
import random
import re


regex_number_filter = r"\s([+-]?[0-9]*[.]?[0-9]{2,})\s"


class Signal:
    # constructor
    def __init__(self, signal):
        self.signal = signal
        self.is_valid = True
        self.entry_target = 0.0
        self.stop_loss = []
        self.symbol = ''
        self.signal_type = ''
        self.take_profits = []
        self.side = '' # BUY OR SELL

    def get_binance_symbol(self):
        if self.symbol is not None:
            return self.symbol.replace('/', '')

    def get_entry(self):
        return self.entries

    def get_stop_loss(self):
        return self.stop_loss

    def get_targets(self):
        return self.targets

    def check_signal_for_criteria(self, filtered_signal):
        if 'EXCHANGES' not in filtered_signal:
            return False
        elif 'ENTRYTARGETS' not in filtered_signal:
            return False
        elif 'SIGNALTYPE' not in filtered_signal:
            return False
        elif 'TAKE-PROFITTARGETS' not in filtered_signal:
            return False
        elif '1)' not in filtered_signal or '2)' not in filtered_signal or '3)' not in filtered_signal or\
                '4)' not in filtered_signal or '5)' not in filtered_signal:
            return False
        elif 'LONG' not in filtered_signal and 'SHORT' not in filtered_signal:
            return False
        return True

    def rnd_t(self, val, add_procent=0.0):
        if val <= 0:
            return None
        part = random.uniform(val * 0.002, val * 0.003)

        if self.signal_type == "SHORT":
            return f'{(val + part) - val * add_procent:.6f}'
        else:
            return f'{(val - part) + val * add_procent:.6f}'

    def rnd_e(self, val):
        if val <= 0:
            return None
        part = random.uniform(val * 0.052, val * 0.054)

        if self.signal_type == "SHORT":
            part2 = random.uniform(val * 0.102, val * 0.104)
            # return f'{(val + part):.6f}/{(val+part2):.6f}'
            return f'{(val + part2):.6f}'
        else:
            part2 = random.uniform(val * 0.104, val * 0.106)
            # return f'{(val - part):.6f}/{(val - part2):.6f}'
            return f'{(val - part2):.6f}'

    def find_symbol(self, list):
        for row in list:
            if '#' in row:
                symbol = re.sub(r'[^\w\/]', '', row)
                return symbol
        return None

    # parses the signal to find entry, target and stop loss values.
    def parse_signal(self):
        filtered_signal = self.signal.replace(' ','').upper()
        if self.check_signal_for_criteria(filtered_signal) is False:
            self.is_valid = False
            return
        first_3_lines = filtered_signal.split('\n')[:3]
        self.symbol = self.find_symbol(first_3_lines)
        if self.symbol == None:
            self.is_valid = False
            return
        # split the signal on blank lines
        new_signal = filtered_signal.split('\n\n')
        if len(new_signal) == 1:
            # if no blank lines exist, split single lines
            new_signal = filtered_signal.split('\n')

        # container for stop loss, entry and targets.
        group = []
        for section in new_signal:
            # blank character at end of section to aid regex pattern matches.
            section += " "

            cleaned_section = section.replace("$", " ").replace("-", "  ")
            if 'SIGNALTYPE' in cleaned_section:
                if 'SHORT' in cleaned_section:
                    self.signal_type = 'SHORT'
                    self.side = 'SELL'
                elif 'LONG' in cleaned_section:
                    self.signal_type = 'LONG'
                    self.side = 'BUY'
                else:
                    print('Тип сигнала не определен')
                    self.is_valid = False
                    return

            if 'ENTRYTARGETS' in cleaned_section:
                r1 = re.findall(
                    regex_number_filter,
                    cleaned_section,
                    flags=re.MULTILINE
                )
                if len(r1):
                    self.entry_target = float(r1[0])
            if 'TAKE' in cleaned_section and 'PROFIT' in cleaned_section :
                r1 = re.findall(
                    "\d+\.\d+",#"",
                    cleaned_section,
                    flags=re.MULTILINE
                )
                if len(r1):
                    for x in r1:
                        if len(self.take_profits) < 5:
                            self.take_profits.append(float(x))
        if len(self.take_profits) < 5 or self.entry_target == 0.0 or self.signal_type == '':
            self.is_valid = False
            return

    def form_new_signal(self):

        self.take_profits[0] = self.rnd_t(self.take_profits[0])
        self.take_profits[1] = self.rnd_t(self.take_profits[1], 0.01)
        self.take_profits[2] = self.rnd_t(self.take_profits[2], 0.025)
        self.take_profits[3] = self.rnd_t(self.take_profits[3], 0.05)
        self.take_profits[4] = self.rnd_t(self.take_profits[4], 0.1)
        self.stop_loss = self.rnd_e(self.entry_target)

        new_signal = \
            f'{self.signal_type}: {self.symbol}\nРиск: Торговый робот (стоп-лосс до 30%).\nЛот: max 5% от депозита.' + \
            f'\nЦели: {self.take_profits[0]} (20%) >> {self.take_profits[1]} (20%) >>' \
            f' {self.take_profits[2]} (20%) >> {self.take_profits[3]} (20%) >>' \
            f' {self.take_profits[4]} (20%).\nСтоп: {self.stop_loss}'

        # new_signal = \
        #     f'{self.signal_type}: {self.symbol}\nРиск: Торговый робот (стоп-лосс до 30%).\nЛот: max 5% от депозита.' + \
        #     f'\nЦели: {self.rnd_t(self.take_profits[0])} (20%) >> {self.rnd_t(self.take_profits[1])} (20%) >>' \
        #     f' {self.rnd_t(self.take_profits[2])} (20%) >> {self.rnd_t(self.take_profits[3], 0.05)} (20%) >>' \
        #     f' {self.rnd_t(self.take_profits[4], 0.1)} (20%).\nСтоп: {self.rnd_e(self.entry_target)}'

        return new_signal


