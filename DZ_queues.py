# Очереди для обмена данными между потоками."
# Цель задания:
#
# Освоить механизмы создания потоков и очередей для обмена данных между ними в Python.
# Практически применить знания, создав и запустив несколько потоков и очередь.
#
#
# Задание:
# Моделирование работы сети кафе с несколькими столиками и потоком посетителей, прибывающих для заказа пищи и уходящих после завершения приема.
#
# Есть сеть кафе с несколькими столиками. Посетители приходят, заказывают еду, занимают столик, употребляют еду и уходят. Если столик свободен, новый посетитель принимается к обслуживанию, иначе он становится в очередь на ожидание.
#
# Создайте 3 класса:
# Table - класс для столов, который будет содержать следующие атрибуты: number(int) - номер стола, is_busy(bool) - занят стол или нет.
#
# Cafe - класс для симуляции процессов в кафе. Должен содержать следующие атрибуты и методы:
#
# 1.	Атрибуты queue - очередь посетителей (создаётся внутри init), tables список столов (поступает из вне).
# 2.	Метод customer_arrival(self) - моделирует приход посетителя(каждую секунду).
# 3.	Метод serve_customer(self, customer) - моделирует обслуживание посетителя. Проверяет наличие свободных столов, в случае наличия стола - начинает обслуживание посетителя (запуск потока), в противном случае - посетитель поступает в очередь. Время обслуживания 5 секунд.
# Customer - класс (поток) посетителя. Запускается, если есть свободные столы.
#
# Так же должны выводиться текстовые сообщения соответствующие событиям:
#
# 1.	Посетитель номер <номер посетителя> прибыл.
# 2.	Посетитель номер <номер посетителя> сел за стол <номер стола>. (начало обслуживания)
# 3.	Посетитель номер <номер посетителя> покушал и ушёл. (конец обслуживания)
# 4.	Посетитель номер <номер посетителя> ожидает свободный стол. (помещение в очередь)
#
#
# Пример работы:
# # Создаем столики в кафе
# table1 = Table(1)
# table2 = Table(2)
# table3 = Table(3)
# tables = [table1, table2, table3]
#
# # Инициализируем кафе
# cafe = Cafe(tables)
#
# # Запускаем поток для прибытия посетителей
# customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
# customer_arrival_thread.start()
#
# # Ожидаем завершения работы прибытия посетителей
# customer_arrival_thread.join()
#
#
# Вывод на консоль (20 посетителей [ограничение выставить в методе customer_arrival]):
# Посетитель номер 1 прибыл
# Посетитель номер 1 сел за стол 1
# Посетитель номер 2 прибыл
# Посетитель номер 2 сел за стол 2
# Посетитель номер 3 прибыл
# Посетитель номер 3 сел за стол 3
# Посетитель номер 4 прибыл
# Посетитель номер 4 ожидает свободный стол
# Посетитель номер 5 прибыл
# Посетитель номер 5 ожидает свободный стол
# ......
# Посетитель номер 20 прибыл
# Посетитель номер 20 ожидает свободный стол
# Посетитель номер 17 покушал и ушёл.
# Посетитель номер 20 сел за стол N.
# Посетитель номер 18 покушал и ушёл.
# Посетитель номер 19 покушал и ушёл.
# Посетитель номер 20 покушал и ушёл.



import threading
import time
import queue

class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False

class Cafe: # Класс Cafe- класс для симуляции процессов в кафе/содержит атрибуты:
    def __init__(self, tables):
        self.tables = tables # tables (список столов)/ Атрибут tables список столов (поступает из вне)
        self.queue = queue.Queue() # queue (очередь посетителей) Атрибут queue - очередь посетителей (создаётся внутри init)

    def customer_arrival(self):
        customer_number = 1
        while customer_number <= 20:  # Limit the number of customers to 20 for demonstration
            print(f"Посетитель номер {customer_number} прибыл")
            customer = Customer(customer_number, self)
            customer_number += 1
            customer.start()
            time.sleep(1)

    def serve_customer(self, customer):
        for table in self.tables:
            if not table.is_busy:
                table.is_busy = True
                print(f"Посетитель номер {customer.customer_number} сел за стол {table.number} (начало обслуживания)")
                time.sleep(5)  # Time to serve the customer
                print(f"Посетитель номер {customer.customer_number} покушал и ушёл (конец обслуживания)")
                table.is_busy = False
                self.check_queue()
                break
        else:
            self.queue.put(customer)
            print(f"Посетитель номер {customer.customer_number} ожидает свободный стол (помещение в очередь)")

    def check_queue(self):
        if not self.queue.empty():
            customer = self.queue.get()
            self.serve_customer(customer)

class Customer(threading.Thread): # Класс Customer наследуется от threading.Thread/ класс (поток) посетителя.
#                                   Запускается, если есть свободные столы.и содержит атрибуты:
    def __init__(self, customer_number, cafe):
        super().__init__()
        self.customer_number = customer_number # customer_number (номер посетителя)
        self.cafe = cafe

    def run(self):  # Метод run запускается при запуске потока и моделирует приход посетителя,
#                                     # прием пищи и уход.
        self.cafe.serve_customer(self)

# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()