import copy
#задание 16


class Row(object):
    countId = 0  # общее кол-ва строк
    variablesNum = 0  # кол-во переменных в строке

    def __init__(self, collection, value):
        Row.countId += 1
        Row.variablesNum = len(collection)
        self.num_1 = 0 # кол-во переменных = 1
        for var in collection:
            if var == 1:
                self.num_1 += 1

        self.value = value  # значение функции
        self.collection = collection  # список со значениями переменных строки
        self.id = Row.countId

    # для копирования строк
    def __copy__(self):
        return type(self)(self.collection, self.value)


class Table(object):

    def __init__(self, rowsNum):
        self.rowsNum = rowsNum  # кол-во строк таблицы (в коде не задействовано)
        self.rows = []  # объекты Row

    def addRow(self, row):
        for x in self.rows:
            if x.id == row.id:
                print("повторяются id строк!")
                return
        self.rows.append(row)

    def setRow(self, row):
        for i in range(0, len(self.rows)):
            if self.rows[i].id == row.id:
                self.rows[i] = row
                return
        print("id строки не найдено!")

    def getRow(self, rowId):
        for x in self.rows:
            if x.id == rowId:
                return x

    def display(self):
        print("id", end="\t")
        for i in range(0, Row.variablesNum):
            print("X%d" % (i+1), end="\t")
        print("\t F")
        for x in self.rows:
            print(x.id, end="\t")
            for var in x.collection:
                print(var, end="\t")
            print('|\t', x.value)


#таблица для подсчёта минимизаций
class Table2(object):

    def __init__(self, firstRows, secondRows, varNum):
        self.varNum = varNum
        self.firstRows = firstRows
        self.secondRows = secondRows
        self.table2 = [['-'] * (len(firstRows)+1) for i in range(len(secondRows)+1)]  # двумерный список для подсчёта минимизаций
        self.table2[0][0] = '#'
        # добавление первоначальных строк
        for i in range(len(secondRows)):
            s = str(secondRows[i])
            s = s.replace('[', '')
            s = s.replace(']', '')
            s = s.replace(',', '')
            s = s.replace(' ', '')
            s = s.replace("'", '')
            self.table2[i+1][0] = s

        # добавление строк c *
        for i in range(len(firstRows)):
            s = str(firstRows[i])
            s = s.replace('[', '')
            s = s.replace(']', '')
            s = s.replace(',', '')
            s = s.replace(' ', '')
            self.table2[0][i+1] = s

    def calculate(self):
        plusesInColumn = {}  # слоарь для подсчёта плюсов в столбцах
        plusesPos = [0] * (len(self.firstRows)+1)  # последний индекс строки, в которой есть плюс
        for j in range(1, len(self.firstRows)+1):
            plusesInColumn.update({j: 0})

        for i in range(1, len(self.secondRows)+1):
            for j in range(1, len(self.firstRows)+1):
                result = True
                for elem in range(self.varNum):
                    if self.table2[i][0][elem] != self.table2[0][j][elem] and self.table2[i][0][elem] != '*':
                        result = False
                        break
                if result:
                    self.table2[i][j] = '+'
                    plusesInColumn[j] += 1
                    plusesPos[j] = i

        isPlusInColumn = [False] * (len(plusesInColumn)+1)  # булевый список для подсчёта, все ли строки взяли
        isPlusInColumn[0] = True
        self.answer = []  # минимизированная функция

        for key in plusesInColumn:
            if plusesInColumn[key] == 1:
                self.answer.append(self.table2[plusesPos[key]][0])
                for i in range(1, len(self.firstRows) + 1):
                    if self.table2[plusesPos[key]][i] == '+':
                        isPlusInColumn[i] = True

        flagExit = True
        # пока взяли не все строки в ответ или пока поняли, что не можем построить функцию:
        while False in isPlusInColumn and flagExit:
            flagExit = False
            num_1 = [0] * (len(self.secondRows) + 1)  # кол-во невошедших в ответ единиц для каждой строки
            # поиск невошедших в ответ единиц для каждой строки
            for i in range(1, len(self.secondRows)+1):
                # если в ответах уже есть эта строка, то пропускаем
                if self.table2[i][0] in self.answer: continue
                for j in range(1, len(self.firstRows)):
                    if self.table2[i][j] == "+" and not isPlusInColumn[j]:
                        num_1[i] += 1

            maxNum_1 = max(num_1)  # максимальное число невошедших в ответ единиц
            # поиск строки с максимальным числом невошедших единиц
            for i in range(1, len(self.secondRows)+1):
                # добавляем строку с максимальным ко-вом единиц
                if num_1[i] == maxNum_1 and not self.table2[i][0] in self.answer:
                    self.answer.append(self.table2[i][0])
                    for j in range(1, len(self.firstRows)+1):
                        if self.table2[i][j] == "+":
                            flagExit = True
                            isPlusInColumn[j] = True
                    break
            if not flagExit:
                break

        # собираем строку - ответ
        stringAnswer = ""
        for i in range(len(self.answer)):
            for j in range(len(self.answer[i])):
                if j != 0 and self.answer[i][j] != '*' and stringAnswer[len(stringAnswer)-1 != '*']:
                    stringAnswer += '*'
                if self.answer[i][j] == '1':
                    stringAnswer += 'X' + str(j+1)
                elif self.answer[i][j] == '0':
                    stringAnswer += "not(X" + str(j+1) + ')'

            if i != len(self.answer)-1:
                stringAnswer += " + "

        return stringAnswer


    # вывод таблицы с '+'
    def display(self):
        for i in range(len(self.secondRows)+1):
            for j in range(len(self.firstRows)+1):
                print(self.table2[i][j], end="\t")
            print()


class LogicFunction:

    def __init__(self, variablesNum, table):
        LogicFunction.table = table  # создание копии таблицы, чтобы выводить строки с "*"
        self.variablesNum = variablesNum  # кол-во переменных
        self.table = table

    # минимизация функции
    def getExpression(self):
        self.sortedRows = copy.deepcopy(self.table.rows)  # глубокое копирование списка строк с таблицы (чтобы не изменить саму таблицу)
        # удаление строк, где значение функции = 0, т.к. будем выбирать из тех, которые = 1
        for row in self.sortedRows:
            if row.value == 0:
                self.sortedRows.remove(row)

        self.sortedRows.sort(key=lambda row: row.num_1)
        flag = True
        while flag:
            flag = False
            self.newRows = []  # создание новых строк с "*"
            self.permanentRows = [True] * len(self.sortedRows)  # булевый список, обозначивающий, есть ли совпадения с каждой строкой
            self.sortedRows.sort(key=lambda row: row.num_1)  # сортировка строк по кол-ву единиц в переменных
            for row1 in range(0, len(self.sortedRows)):
                for row2 in range(row1+1, len(self.sortedRows)):
                    if self.sortedRows[row2].num_1 - self.sortedRows[row1].num_1 > 1: break  # переходим к следующей итерации, если строки отличаются кол-вом единиц > 1
                    differNum = 0  # кол-во различающихся переменных
                    differPos = 0  # номер последней оличающейся переменной
                    for i in range(self.variablesNum):
                        # если переменные в строках различаются, увеличиваем свётчик
                        if self.sortedRows[row1].collection[i] != self.sortedRows[row2].collection[i]:
                            differNum += 1
                            differPos = i

                    if differNum == 1:
                        if self.sortedRows[row1].collection[differPos] == '*' or self.sortedRows[row2].collection[differPos] == '*': continue
                        self.permanentRows[row1] = False  # для этих строк уже нашли совпадение
                        self.permanentRows[row2] = False
                        newRow = copy.deepcopy(self.sortedRows[row1])  # создание новой строки из двух
                        newRow.collection[differPos] = '*'
                        if newRow not in self.newRows:
                            self.newRows.append(newRow)  # добавление новой строки
                        flag = True  # обновляем флаг для следующего прохода цикла

            # если не нашли совпадений, то добавляем в новый список
            for i in range(0, len(self.sortedRows)):
                if self.permanentRows[i]:
                    self.newRows.append(self.sortedRows[i])

            self.sortedRows = self.newRows.copy()  # присваиваем сортирующимся строкам новые строки

        if len(self.sortedRows) == 0:
            print("Не удалось вычислить формулу! Введите хотя бы одну строку со значением функции = 1!")
            return

        # делаем строки из списков
        listFirstRows = [x.collection for x in self.table.rows]
        stringFirstRows = [''.join(str(x)) for x in listFirstRows]
        listSecondRows = [x.collection for x in self.sortedRows]
        stringSecondRows = [''.join(str(x)) for x in listSecondRows]
        self.table2 = Table2(stringFirstRows, stringSecondRows, self.variablesNum)
        print("\nF = ", self.table2.calculate())  # вывод результата

    # вывод таблицы с *
    def getTable(self):
        for x in self.sortedRows:
            for i in x.collection:
                print(i, end=" ")
            print()
        print()

    def printTable(self):
        self.table.display()


# кол-во переменных в строках должно быть одинаковым!
row = Row([1, 0, 0], 1)
row2 = Row([1, 1, 0], 1)
row3 = Row([1, 0, 0], 1)
row4 = Row([0, 1, 1], 0)
table = Table(3)  # создаём новую таблицу с передачей кол-ва строк (в коде не задействовано)
table.addRow(row)
table.addRow(row2)
table.addRow(row3)
table.addRow(row4)
func = LogicFunction(3, table)  # вызываем минимизацию функции с передачей кол-ва переменных и таблицы истинности
func.printTable()  # выводим таблицу истинности
func.getExpression()  # вычисление и вывод получившейся функции