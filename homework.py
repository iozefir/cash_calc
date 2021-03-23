import datetime as dt


class Record:
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount,
                 date=None,
                 comment=''):
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()
        self.amount = amount
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record_add):
        self.records.append(record_add)

    def get_today_stats(self):
        today_stats = []
        day = dt.date.today()
        for i in self.records:
            if i.date == day:
                today_stats.append(i.amount)
        return sum(today_stats)

    def get_week_stats(self):
        week_stats = 0
        today_day = dt.date.today()
        week_past = today_day - dt.timedelta(weeks=1)
        for i in self.records:
            if week_past < i.date <= today_day:
                week_stats += i.amount
        return week_stats

    def get_balance(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        balance = self.get_balance()
        if balance > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    'калорийностью не более '
                    f'{balance} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 72.3
    EURO_RATE = 85.6
    RUB_RATE = 1

    def get_today_cash_remained(self, currency):
        currencies_data = {'rub': ('руб', self.RUB_RATE),
                           'usd': ('USD', self.USD_RATE),
                           'eur': ('Euro', self.EURO_RATE)}
        cash = self.get_balance() / currencies_data[currency][1]
        if cash == 0:
            return 'Денег нет, держись'
        cash = round(cash, 2)
        currency_str = currencies_data[currency][0]
        if cash > 0:
            return ('На сегодня осталось'
                    f' {cash} {currency_str}')
        cash_debt = abs(cash)
        return ('Денег нет, держись: твой долг - '
                f'{cash_debt} {currency_str}')
