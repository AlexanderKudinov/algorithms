# задания 25, 26, 27


# кодирование текста методом Хаффмана
def encodeHuffman(fileIn, fileOut):
    fileText = open(fileIn, 'r')
    fileDictionary = open("dictionary.txt", 'w')
    fileHuff = open(fileOut, 'w')
    string = fileText.read()  # чтение всего текстового файла
    firstSize = len(string) * 8  # размер текста в битах
    amountSymb = {}  # словарь для подсчёта символов
    # заполнение словаря
    for symb in string:
        if symb in amountSymb:
            amountSymb[symb] += 1
        else:
            amountSymb.update({symb: 1})

    symbols = list(Tree(amount, symb) for symb, amount in amountSymb.items())  # создание списка листьев из символов
    queue = Queue()
    # добавление листьев в очередь
    for x in symbols:
        queue.add(x)

    # поочерёдно соединям листья в одно дерево с помощью очереди
    while queue.getSize() > 1:
        newTree = Tree().concat(queue.pop(), queue.pop())
        queue.add(newTree)

    codesDictionary = {}  # коды для каждого символа
    finalTree = queue.pop()  # результирующее дерево
    finalTree.getCodes(finalTree, codesDictionary)  # получаем коды для каждого символа
    # запись кодов для каждого символа в файл
    for symbols, codes in codesDictionary.items():
        fileDictionary.write(symbols)
        fileDictionary.writelines(":" + codes + "\n")

    # преобразуем символы в коды и записываем в файл
    for symbol in string:
        string = string.replace(symbol, codesDictionary[symbol])

    secondSize = len(string)  # размер закодированного текста в битах
    print("Коэффициент сжатия методом Хаффмана = ", firstSize/secondSize)

    fileHuff.write(string)
    fileHuff.close()
    fileText.close()
    fileDictionary.close()
    return True


# декодирование текста методом Хаффмана
def decodeeHuffman(fileIn, fileOut):
    fileHuff = open(fileIn, 'r')
    fileDecoded = open(fileOut, 'w')
    fileDictionary = open("dictionary.txt", 'r')
    codes = {}
    isEnter = False  # флаг для замены переноса строки на символ
    # читаем словарь с кодами каждого символа из файла
    for line in fileDictionary.readlines():
        if isEnter:
            line = "\\n" + line
            isEnter = False
        pair = line.split(':')
        if (pair[0] == "\n"):
            isEnter = True
        else:
            pair[1] = pair[1].replace("\n",'')
            codes.update({pair[1]: pair[0]})

    string = fileHuff.read()
    codeSequence = ""
    newString = ""
    # подставляем вместо кодов символы и записываем в файл новую строку
    for i in range(len(string)):
        codeSequence += string[i]
        if codeSequence in codes:
            # если это символ переноса строки, то заменяем
            if codes[codeSequence] == "\\n":
                newString += "\n"
            else:
                newString += codes[codeSequence]
            codeSequence = ""

    fileDecoded.write(newString)
    fileDictionary.close()
    fileDecoded.close()
    fileHuff.close()
    return True


# кодирование текста методом Лемпеля-Зива
def encodeLZ(fileIn, fileOut):
    fileText = open(fileIn, 'r')
    fileLZ = open(fileOut, 'w')
    text = fileText.read()
    dictFirst = {}  # словарь для запоминания {первоначальная последовательность: номер}
    dictSecond = {}  # словарь для запоминания {номер: закодированная последовательность}
    tempString = ""  # временная последовательность символов
    numPrev = -1  # номер последовательности, на которую ссылается текущая
    numElements = 0  # сколько элементов находится в словаре
    firstSize = len(text)  # размер текста в байтах

    # добавление уникальных последовательностей в словарь
    for symbol in text:
        tempString += symbol
        # если последовательность уже есть в словаре, то запоминаем её номер
        if tempString in dictFirst:
            numPrev = dictFirst[tempString]
        # иначе добавляем в два словаря
        else:
            numElements += 1
            dictFirst.update({tempString: numElements})  # добавляем в словарь {первоначальная последовательность: номер}
            # добавляем в словарь {номер: закодированная последовательность}
            if numPrev == -1:
                dictSecond.update({numElements: tempString[-1]})
            else:
                dictSecond.update({numElements: str(numPrev) + tempString[-1]})
            tempString = ""
            numPrev = -1  # останется -1, если это будет уникальный символ

    secondSize = 0  # размер закодированного текста в байтах
    for value in dictSecond.values():
        fileLZ.write(value)
        secondSize += len(value)
    # если не включили последнюю последовательность, добавляем
    if (tempString != ""):
        fileLZ.write(str(dictFirst[tempString]))
        secondSize += len(str(dictFirst[tempString]))

    print("Коэффициент сжатия методом Лемпеля-Зива = ", firstSize / secondSize)
    fileLZ.close()
    fileText.close()
    return True


# декодирование текста методом Лемпеля-Зива
def decodeLZ(fileIn, FileOut):
    fileLZ = open(fileIn, 'r')
    fileDecoded = open(FileOut, 'w')
    code = fileLZ.read()  # закодированная последовательность
    dictCode = {}  # словарь для запоминания {номер: закодированная последовательность}
    tempString = ""  # временная последовательность символов
    numPrev = 0  # номер последовательности, на которую ссылается текущая
    numElements = 0  # сколько элементов находится в словаре

    #декодируем последовательность
    for symbol in code:
        # если это буква
        if symbol.isalpha():
            numElements += 1
            if len(tempString) == 0:
                numPrev = 0
            else:
                numPrev = int(tempString)
            tempString = ""
            # если элемент ни на кого не ссылается
            if (numPrev == 0):
                dictCode.update({numElements: symbol})
            else:
                dictCode.update({numElements: dictCode[numPrev] + symbol})
        # если это цифра
        else:
            tempString += symbol

    # записываем в файл декодированный текст
    for value in dictCode.values():
        fileDecoded.write(value)
    # если пропустили последний символ
    if tempString != "":
        fileDecoded.write(dictCode[int(tempString)])

    fileDecoded.close()
    fileLZ.close()
    return True


# для алгоритма Хаффмана
# в дереве содержится вес и значение элемента, вес нужен для очереди с приоритетом
class Tree(object):
    # создание дерева с единственным листом
    def __init__(self, weight = 0, value = 0):
        self.weight = weight  # вес элемента
        self.value = value  # кол-во этих символов
        self.left = 0  # левый лист
        self.right = 0  # правый лист

    # объединение листов
    def concat(self, leftLeef, rightLeef):
        parent = Tree(leftLeef.weight + rightLeef.weight)
        parent.left = leftLeef
        parent.right = rightLeef
        parent.value = 0
        return parent

    """
    # вывод дерева на экран
    def print(self, parent):
        # запуск по левым потомкам
        if parent.left != 0:
            self.print(parent.left)
        # печать самого себя
        elif parent.value != 0:
            print(parent.value, ':', parent.weight)
        # запуск по правым потомкам
        if parent.right != 0:
            self.print(parent.right)
    """

    def getCodes(self, parent, listCodes, string = ""):
        # запуск по левым потомкам
        if parent.left != 0:
            self.getCodes(parent.left, listCodes, string + '0')
        # добавление нового кода
        elif parent.value != 0:
            listCodes.update({parent.value: string})

        # запуск по правым потомкам
        if parent.right != 0:
            self.getCodes(parent.right, listCodes, string + '1')


#для алгоритма Хаффмана
#очередь с приоритетом, на основе списка (содержит листья дерева)
class Queue(object):
    List = []
    # добавляем лист в очередь
    def add(self, elem):
        for i in range(0, len(Queue.List)):
            # если вес вставляемого элемента <= текущего, то вставляем и выходим
            if (elem.weight <= Queue.List[i].weight):
                Queue.List.insert(i, elem)
                return

        # если вес вставляемого элемента > всех остальных в очереди, вставляем в конец
        Queue.List.append(elem)

    # извлекает и удаляет первый элемент очереди
    def pop(self):
        if self.getSize() > 0:
            return Queue.List.pop(0)

    # вывод очереди на экран
    def print(self):
        for elem in Queue.List:
            elem.print(elem)

    # получить размер очереди
    def getSize(self):
        return len(Queue.List)


encodeHuffman("FileTextForHuffman.txt", "FileHuffmanForText.txt")
decodeeHuffman("FileHuffmanForText.txt", "FileDecodedHuff.txt")
encodeLZ("FileTextForLZ.txt", "fileLZForText.txt")
decodeLZ("FileLZForText.txt", "FileDecodedLZ.txt")


