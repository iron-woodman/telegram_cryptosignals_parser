# -*- coding: utf-8 -*-
import random


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
        if 'LONG' not in filtered_signal and 'SHORT' not in filtered_signal:
            return False
        return True

    def rnd_t(self, entry_point, add_procent1, add_procent2):
        """
        расчет тейк-профита
        :param entry_point: точка входа
        :param add_procent1: нижниее значение случайного диапазона
        :param add_procent2: верхнее значение случайного диапазона
        :return:
        """
        if entry_point <= 0:
            return None
        add_procent = random.uniform(add_procent1, add_procent2)

        if self.signal_type == "SHORT":
            return f'{entry_point - entry_point * add_procent:.6f}'
        else:
            return f'{entry_point + entry_point * add_procent:.6f}'

    def rnd_e(self, entry_point, add_procent1, add_procent2):
        """
        расчет стоп-лосса
        :param entry_point: точка входа
        :param add_procent1: нижниее значение случайного диапазона
        :param add_procent2: верхнее значение случайного диапазона
        :return:
        """
        if entry_point <= 0:
            return None
        add_procent = random.uniform(add_procent1, add_procent2)

        if self.signal_type == "SHORT":
            return f'{(entry_point + entry_point * add_procent):.6f}'
        else:
            return f'{(entry_point - entry_point * add_procent):.6f}'


    # parses the signal to find entry, target and stop loss values.
    def parse_signal(self):
        filtered_signal = self.signal.replace(' ', '').upper().replace(',', '.')
        if self.check_signal_for_criteria(filtered_signal) is False:
            self.is_valid = False
            return
        signal_lines = filtered_signal.split('\n')
        if len(signal_lines) < 3:
            print('Неверный формат исходного сигнала.')
            self.is_valid = False
            return

        self.symbol = signal_lines[0].replace(' ', '')
        if self.symbol == None:
            self.is_valid = False
            return
        if 'SHORT' in signal_lines[1]:
            self.signal_type = 'SHORT'
            self.side = 'SELL'
        elif 'LONG' in signal_lines[1]:
            self.signal_type = 'LONG'
            self.side = 'BUY'
        else:
            print('Тип сигнала не определен.')
            self.is_valid = False
            return

        self.entry_target = float(signal_lines[2].replace(' ', ''))

    def signal_icon(self):
        if self.signal_type == "LONG":
            return "📈"
        else:
            return  "📉"


    def form_new_signal(self):
        self.take_profits.clear()
        self.take_profits.append(self.rnd_t(self.entry_target, 0.0085, 0.0105))
        self.take_profits.append(self.rnd_t(self.entry_target, 0.0225, 0.025))
        self.take_profits.append(self.rnd_t(self.entry_target, 0.0415, 0.045))
        self.take_profits.append(self.rnd_t(self.entry_target, 0.0855, 0.09))
        self.take_profits.append(self.rnd_t(self.entry_target, 0.14, 0.145))

        self.stop_loss = self.rnd_e(self.entry_target, 0.11, 0.115)

        new_signal = \
            f'{self.signal_icon()} {self.signal_type}: {self.symbol}/USDT\n❗️Лот: max 0.33% от депозита.' + \
            f'\n🎯Цели:\n1) {self.take_profits[0]} (20%)\n2) {self.take_profits[1]} (20%)' \
            f'\n3) {self.take_profits[2]} (20%)\n4) {self.take_profits[3]} (20%)' \
            f'\n5) {self.take_profits[4]} (20%).\n⛔️Стоп: {self.stop_loss}'

        return new_signal


