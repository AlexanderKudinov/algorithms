# задание 15
# Код Хэмминга


class HammingEncoder(object):

    def __init__(self, dataBits):
        self.dataBits = dataBits  # кол-во информационных разрядов
        self.controlBits = 0  # кол-во контрольных битов

    def encode(self, str):
        self.encodeString = ""
        newString = ""
        chetStrBit = 0  # счетчик по битам первоначальной строки
        degree_2 = 1  # степени двойки
        i = 0
        # вставка контрольных битов = 0
        while i < self.controlBits + self.dataBits:
            if (i+1) % degree_2 == 0:
                degree_2 *= 2
                newString += '0'
                self.controlBits += 1
            else:
                if chetStrBit >= len(str): break
                newString += str[chetStrBit]
                chetStrBit += 1
            i += 1

        degree_2 = 1
        # устанавливаем значения контрольным битам
        for i in range(1, len(newString)+1):
            if i % degree_2 == 0:
                degree_2 *= 2
                bit = -1
                for j in range(i, len(newString), i*2):
                    for k in range(j, j+i):
                        if k >= len(newString)+1: break
                        if k == i: continue
                        if bit == -1:
                            bit = int(newString[k-1])
                        else:
                            bit = bit ^ int(newString[k-1])

                if bit == -1:
                    self.encodeString += newString[i-1]
                else:
                    self.encodeString += bit.__str__()
            else:
                self.encodeString += newString[i-1]

        return self.encodeString

    def decode(self, str):
        strMistake = ""
        self.decodeString = ""
        rightString = str  # строка без ошибок
        degree_2 = 1
        for i in range(1, len(str)+1):
            if i % degree_2 == 0:
                degree_2 *= 2
                bit = -1
                for j in range(i, len(str), i*2):
                    for k in range(j, j+i):
                        if k >= len(str)+1: break
                        if bit == -1:
                            bit = int(str[k-1])
                        else:
                            bit = bit ^ int(str[k-1])

                strMistake += bit.__str__()

        posMistake = int(strMistake)-1  # позиция ошибки
        if posMistake != -1:
            rightString = str[0:posMistake] + str((int(str[posMistake])+1)%2) + str[posMistake+1:]  # исправляем ошибку

        degree_2 = 1
        # удаляем контрольные биты
        for i in range(len(str)):
            if (i+1) % degree_2 != 0:
                self.decodeString += str[i]
            else:
                degree_2 *= 2

        return self.decodeString


Hamming = HammingEncoder(8)
s = Hamming.encode("01000100")
print("Закодированная последовательность:")
print(s, "\n\n")
s2 = Hamming.decode(s)
print("Декодированная последовательность:")
print(s2, "\n\n")