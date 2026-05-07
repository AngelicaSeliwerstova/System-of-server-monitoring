class LogEvent:
    def __init__(self, time: str, level: str, source: str, message: str):
        self.time = time
        self.level = level
        self.source = source
        self.message = message

    def is_error(self):
        return self.level == "ERROR"

    def __repr__(self):
        return f"{self.time} {self.level} {self.source} {self.message}"


class ServerMonitor:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def count_errors(self):
        error_count = 0

        for event in self.events:
            if event.level == "ERROR":
                error_count += 1

        return error_count

    def count_info(self):
        info_count = 0

        for event in self.events:
            if event.level == "INFO":
                info_count += 1

        return info_count

    def count_warnings(self):
        warning_count = 0

        for event in self.events:
            if event.level == "WARNING":
                warning_count += 1

        return warning_count

    def most_problematic_source(self):
        sources = {}

        for eventy in self.events:
            if eventy.level == "ERROR":
                if eventy.source in sources:
                    sources[eventy.source] += 1
                else:
                    sources[eventy.source] = 1
        if len(sources) == 0:
            return "Ошибок нет"
        max_source = None
        max_count = 0
        for source in sources:
            if sources[source] > max_count:
                max_count = sources[source]
                max_source = source

        return max_source

    def filter_by_level(self, level):
        filtred_events = []
        for eventp in self.events:
            if eventp.level == level:
                filtred_events.append(eventp)
        return filtred_events

    def filter_by_source(self, source):
        filtred_2_events = []
        for eventp in self.events:
            if eventp.source == source:
                filtred_2_events.append(eventp)
        return filtred_2_events

    def last_error(self):
        for event in reversed(self.events):
            if event.level == "ERROR":
                return event
        return "Ошибок нет"

    def show_report(self):
        print("Всего событий:", len(self.events))


class Report:
    def __init__(self, monitor):
        self.monitor = monitor

    def show(self):
        print("=== SERVER REPORT ===")
        print("Всего событий:", len(self.monitor.events))
        print("ERROR:", self.monitor.count_errors())
        print("WARNING:", self.monitor.count_warnings())
        print("INFO:", self.monitor.count_info())
        print("Статус:", self.status())
        print("Самый проблемый модуль:", self.monitor.most_problematic_source())
        print("События:")
        for event in self.monitor.events:
            print(event)
        print("Последняя ошибка:", self.monitor.last_error())

    def status(self):
        errors = self.monitor.count_errors()
        warnings = self.monitor.count_warnings()
        if errors >= 3:
            return "CRITICAL"
        elif errors >= 1:
            return "UNSTABLE"
        elif warnings >= 3:
            return "WARNING"
        else:
            return "OK"

    def show_events(self, events):
        if len(events) == 0:
            print("Событий не найдено")
            return

        for event in events:
            print(event)


log1 = LogEvent("12:05", "WARNING", "database", "slow query")

log2 = LogEvent("12:07", "ERROR", "database", "connection failed")
log3 = LogEvent("12:10", "INFO", "api", "request completed")

monitor = ServerMonitor()
monitor.add_event(log1)
monitor.add_event(log2)
monitor.add_event(log3)

report = Report(monitor)
print("Моя госпожа, что показать?")
print("1-Полный отчет")
print("2-Только ERRORS")
print("3-Только WARNINGS")
print("4-Только INFO")
print("5-События конкретного модуля")
choise = input("Введите номер: ")
if choise == "1":
    report.show()
elif choise == "2":
    print("===ERROR_EVENTS===")
    report.show_events(monitor.filter_by_level("ERROR"))
elif choise == "3":
    print("===WARNING_EVENTS===")
    report.show_events(monitor.filter_by_level("WARNING"))
elif choise == "4":
    print("===INFO_EVENTS===")
    report.show_events(monitor.filter_by_level("INFO"))
elif choise == "5":
    source = input("введите событие конкретного модуля,например,datbase,ap: ")
    print(f"===EVENTS_FROM {source} ===")
    report.show_events((monitor.filter_by_source(source)))
else:
    print("Выберите вариант из списка")
