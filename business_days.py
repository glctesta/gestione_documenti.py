"""
Modulo per la gestione dei giorni lavorativi e festività.
Utilizzabile da tutti i moduli che inviano notifiche automatiche.
"""

from datetime import date, datetime
import logging

logger = logging.getLogger(__name__)


class BusinessDayChecker:
    """
    Classe per verificare se una data è un giorno lavorativo.
    Gestisce weekend e festività canoniche.
    """

    # Festività fisse (formato: (mese, giorno))
    FIXED_HOLIDAYS = [
        (1, 1),  # Capodanno
        (1, 6),  # Epifania
        (5, 1),  # Festa dei Lavoratori
        (8, 15),  # Ferragosto
        (11, 1),  # Ognissanti
        (12, 1),  # Festa nazionale rumena
        (12, 25),  # Natale
        (12, 26),  # Santo Stefano
    ]

    def __init__(self, additional_holidays=None, country_code='IT'):
        """
        Inizializza il checker.

        :param additional_holidays: Lista di date aggiuntive (datetime.date o str 'YYYY-MM-DD')
        :param country_code: Codice paese per festività specifiche ('IT', 'RO', 'US', ecc.)
        """
        self.country_code = country_code
        self.additional_holidays = self._parse_additional_holidays(additional_holidays or [])

        # Carica festività specifiche per paese
        self._load_country_holidays()

    def _parse_additional_holidays(self, holidays):
        """Converte le festività aggiuntive in oggetti date"""
        parsed = []
        for h in holidays:
            if isinstance(h, date):
                parsed.append(h)
            elif isinstance(h, str):
                try:
                    parsed.append(datetime.strptime(h, '%Y-%m-%d').date())
                except ValueError:
                    logger.warning(f"Formato data non valido: {h}")
        return parsed

    def _load_country_holidays(self):
        """Carica festività specifiche per paese"""
        if self.country_code == 'RO':
            # Romania
            self.FIXED_HOLIDAYS.extend([
                (1, 2),  # Giorno dopo Capodanno
                (1, 24),  # Unirea Principatelor Române
                (5, 1),  # Ziua Muncii
                (12, 1),  # Ziua Națională
            ])
        elif self.country_code == 'US':
            # USA (esempi)
            self.FIXED_HOLIDAYS.extend([
                (7, 4),  # Independence Day
                (11, 11),  # Veterans Day
            ])
        # Aggiungi altri paesi se necessario

    def is_weekend(self, check_date=None):
        """
        Verifica se la data è un weekend (sabato o domenica).

        :param check_date: Data da verificare (default: oggi)
        :return: True se è weekend
        """
        if check_date is None:
            check_date = date.today()
        elif isinstance(check_date, datetime):
            check_date = check_date.date()

        return check_date.weekday() >= 5  # 5=Sabato, 6=Domenica

    def is_fixed_holiday(self, check_date=None):
        """
        Verifica se la data è una festività fissa.

        :param check_date: Data da verificare (default: oggi)
        :return: True se è festività fissa
        """
        if check_date is None:
            check_date = date.today()
        elif isinstance(check_date, datetime):
            check_date = check_date.date()

        return (check_date.month, check_date.day) in self.FIXED_HOLIDAYS

    def is_additional_holiday(self, check_date=None):
        """
        Verifica se la data è nelle festività aggiuntive.

        :param check_date: Data da verificare (default: oggi)
        :return: True se è festività aggiuntiva
        """
        if check_date is None:
            check_date = date.today()
        elif isinstance(check_date, datetime):
            check_date = check_date.date()

        return check_date in self.additional_holidays

    def is_easter(self, check_date=None):
        """
        Verifica se la data è Pasqua o Lunedì dell'Angelo.
        Usa l'algoritmo di Gauss per calcolare la Pasqua.

        :param check_date: Data da verificare (default: oggi)
        :return: True se è Pasqua o Lunedì dell'Angelo
        """
        if check_date is None:
            check_date = date.today()
        elif isinstance(check_date, datetime):
            check_date = check_date.date()

        year = check_date.year
        easter_date = self._calculate_easter(year)

        # Calcola Lunedì dell'Angelo
        from datetime import timedelta
        easter_monday = easter_date + timedelta(days=1)

        return check_date in [easter_date, easter_monday]

    def _calculate_easter(self, year):
        """
        Calcola la data della Pasqua usando l'algoritmo di Gauss.

        :param year: Anno
        :return: Data della Pasqua
        """
        a = year % 19
        b = year // 100
        c = year % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        month = (h + l - 7 * m + 114) // 31
        day = ((h + l - 7 * m + 114) % 31) + 1

        return date(year, month, day)

    def is_business_day(self, check_date=None):
        """
        Verifica se la data è un giorno lavorativo.

        :param check_date: Data da verificare (default: oggi)
        :return: True se è giorno lavorativo
        """
        if check_date is None:
            check_date = date.today()
        elif isinstance(check_date, datetime):
            check_date = check_date.date()

        # Verifica tutte le condizioni
        if self.is_weekend(check_date):
            logger.debug(f"{check_date} è un weekend")
            return False

        if self.is_fixed_holiday(check_date):
            logger.debug(f"{check_date} è una festività fissa")
            return False

        if self.is_easter(check_date):
            logger.debug(f"{check_date} è Pasqua o Lunedì dell'Angelo")
            return False

        if self.is_additional_holiday(check_date):
            logger.debug(f"{check_date} è una festività aggiuntiva")
            return False

        return True

    def get_holiday_name(self, check_date=None):
        """
        Restituisce il nome della festività (se applicabile).

        :param check_date: Data da verificare (default: oggi)
        :return: Nome festività o None
        """
        if check_date is None:
            check_date = date.today()
        elif isinstance(check_date, datetime):
            check_date = check_date.date()

        if self.is_weekend(check_date):
            return "Sabato" if check_date.weekday() == 5 else "Domenica"

        # Dizionario festività
        holiday_names = {
            (1, 1): "Capodanno",
            (1, 6): "Epifania",
            (4, 25): "Festa della Liberazione",
            (5, 1): "Festa dei Lavoratori",
            (6, 2): "Festa della Repubblica",
            (8, 15): "Ferragosto",
            (11, 1): "Ognissanti",
            (12, 8): "Immacolata Concezione",
            (12, 25): "Natale",
            (12, 26): "Santo Stefano",
        }

        key = (check_date.month, check_date.day)
        if key in holiday_names:
            return holiday_names[key]

        if self.is_easter(check_date):
            easter = self._calculate_easter(check_date.year)
            if check_date == easter:
                return "Pasqua"
            else:
                return "Lunedì dell'Angelo"

        return None


# ========================================
# 🎯 FUNZIONI DI UTILITÀ GLOBALI
# ========================================

def is_business_day(check_date=None, country_code='IT', additional_holidays=None):
    """
    Funzione di utilità per verificare rapidamente se è un giorno lavorativo.

    Args:
        check_date: Data da verificare (default: oggi)
        country_code: Codice paese ('IT', 'RO', ecc.)
        additional_holidays: Lista di festività aggiuntive

    Returns:
        bool: True se è giorno lavorativo

    Example:
        >>> from datetime import date
        >>> # Test con un venerdì normale
        >>> is_business_day(date(2025, 11, 7))
        True
        >>> # Test con un sabato
        >>> is_business_day(date(2025, 11, 8))
        False
    """
    checker = BusinessDayChecker(additional_holidays=additional_holidays, country_code=country_code)
    return checker.is_business_day(check_date)


def should_send_notification(check_date=None, country_code='IT', additional_holidays=None):
    """
    Alias più esplicito per verificare se inviare notifiche.

    Args:
        check_date: Data da verificare (default: oggi)
        country_code: Codice paese
        additional_holidays: Lista di festività aggiuntive

    Returns:
        bool: True se si può inviare la notifica

    Example:
        >>> from datetime import date
        >>> should_send_notification(date(2025, 12, 25))  # Natale
        False
        >>> should_send_notification(date(2025, 11, 7))  # Venerdì normale
        True
    """
    return is_business_day(check_date, country_code, additional_holidays)


def count_business_days_between(start_date, end_date, country_code='IT', additional_holidays=None):
    """
    Conta i giorni lavorativi tra due date (estremi esclusi).
    Utile per calcolare quanti giorni lavorativi sono trascorsi da una data.

    Args:
        start_date: Data di inizio (date, datetime o str 'YYYY-MM-DD')
        end_date: Data di fine (date, datetime o str 'YYYY-MM-DD', default: oggi)
        country_code: Codice paese
        additional_holidays: Lista di festività aggiuntive

    Returns:
        int: Numero di giorni lavorativi tra start_date ed end_date (esclusi).

    Example:
        >>> from datetime import date
        >>> count_business_days_between(date(2025, 11, 7), date(2025, 11, 12))  # ven->mer
        3
    """
    from datetime import timedelta

    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    elif isinstance(start_date, datetime):
        start_date = start_date.date()

    if end_date is None:
        end_date = date.today()
    elif isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    elif isinstance(end_date, datetime):
        end_date = end_date.date()

    checker = BusinessDayChecker(additional_holidays=additional_holidays, country_code=country_code)

    count = 0
    current = start_date + timedelta(days=1)
    max_iterations = 365
    while current < end_date and max_iterations > 0:
        if checker.is_business_day(current):
            count += 1
        current += timedelta(days=1)
        max_iterations -= 1
    return count


def get_business_days_since(start_date, country_code='IT', additional_holidays=None):
    """
    Conta i giorni lavorativi trascorsi da start_date fino a oggi.

    Args:
        start_date: Data di inizio
        country_code: Codice paese
        additional_holidays: Lista di festività aggiuntive

    Returns:
        int: Giorni lavorativi trascorsi.
    """
    return count_business_days_between(start_date, date.today(), country_code, additional_holidays)


def get_next_business_day(start_date=None, country_code='IT', additional_holidays=None):
    """
    Trova il prossimo giorno lavorativo.

    Args:
        start_date: Data di partenza (default: oggi)
        country_code: Codice paese
        additional_holidays: Lista di festività aggiuntive

    Returns:
        date: Prossimo giorno lavorativo

    Example:
        >>> from datetime import date
        >>> # Da venerdì -> lunedì
        >>> get_next_business_day(date(2025, 11, 7))
        datetime.date(2025, 11, 10)
        >>> # Da giovedì -> venerdì
        >>> get_next_business_day(date(2025, 11, 6))
        datetime.date(2025, 11, 7)
    """
    from datetime import timedelta

    if start_date is None:
        start_date = date.today()
    elif isinstance(start_date, datetime):
        start_date = start_date.date()

    checker = BusinessDayChecker(additional_holidays=additional_holidays, country_code=country_code)

    current = start_date + timedelta(days=1)
    max_iterations = 30  # Evita loop infiniti

    for _ in range(max_iterations):
        if checker.is_business_day(current):
            return current
        current += timedelta(days=1)

    logger.warning("Impossibile trovare giorno lavorativo nei prossimi 30 giorni")
    return current


# ========================================
# 🧪 TEST (esegui con: python business_days.py)
# ========================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("=" * 60)
    print("TEST MODULO BUSINESS DAYS")
    print("=" * 60)

    checker = BusinessDayChecker(country_code='IT')

    # Test date specifiche
    test_dates = [
        date(2025, 11, 7),  # Venerdì normale
        date(2025, 11, 8),  # Sabato
        date(2025, 11, 9),  # Domenica
        date(2025, 12, 25),  # Natale
        date(2025, 12, 26),  # Santo Stefano
        date(2025, 1, 1),  # Capodanno
        date(2025, 4, 20),  # Pasqua 2025
        date(2025, 4, 21),  # Lunedì dell'Angelo 2025
    ]

    print("\n📅 Test date specifiche:")
    print("-" * 60)
    for test_date in test_dates:
        is_business = checker.is_business_day(test_date)
        holiday_name = checker.get_holiday_name(test_date)

        status = "✅ LAVORATIVO" if is_business else "❌ NON LAVORATIVO"
        extra = f" ({holiday_name})" if holiday_name else ""

        day_name = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"][test_date.weekday()]
        print(f"{test_date.strftime('%d/%m/%Y')} {day_name:10s}: {status}{extra}")

    print("\n" + "=" * 60)
    today = date.today()
    today_status = "✅ Invia notifiche" if is_business_day() else "❌ NON inviare"
    print(f"Oggi ({today.strftime('%d/%m/%Y')}): {today_status}")

    next_day = get_next_business_day()
    print(f"Prossimo giorno lavorativo: {next_day.strftime('%d/%m/%Y')}")
    print("=" * 60)

    # Test con festività personalizzate
    print("\n🎯 Test con festività aziendali personalizzate:")
    print("-" * 60)

    company_holidays = [
        date(2025, 12, 24),  # Vigilia
        date(2025, 12, 31),  # San Silvestro
    ]

    test_date = date(2025, 12, 24)
    result = should_send_notification(test_date, additional_holidays=company_holidays)
    print(f"24/12/2025 (Vigilia aziendale): {'✅ Invia' if result else '❌ NON inviare'}")

    test_date = date(2025, 12, 23)
    result = should_send_notification(test_date, additional_holidays=company_holidays)
    print(f"23/12/2025 (Giorno normale): {'✅ Invia' if result else '❌ NON inviare'}")

    print("=" * 60)
    print("✅ Test completati con successo!")
