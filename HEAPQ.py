class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

class HEAPQ:
    @staticmethod
    def build_huffman_tree(data):
        # Подсчитываем частоту каждого байта
        frequency = {}
        for byte in data:
            if byte in frequency:
                frequency[byte] += 1
            else:
                frequency[byte] = 1

        # Строим список узлов для каждого байта
        heap = [Node(byte, freq) for byte, freq in frequency.items()]

        # Функция для извлечения минимального элемента из списка
        def extract_min(heap):
            min_index = 0
            for i in range(1, len(heap)):
                if heap[i].freq < heap[min_index].freq:
                    min_index = i
            return heap.pop(min_index)

        # Строим дерево Хаффмана
        while len(heap) > 1:
            left = extract_min(heap)
            right = extract_min(heap)

            merged = Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right

            heap.append(merged)

        return heap[0]  # Корень дерева

    @staticmethod
    def generate_codes(node, prefix='', codebook=None):
        if codebook is None:
            codebook = {}

        if node is not None:
            if node.char is not None:
                codebook[node.char] = prefix
            HEAPQ.generate_codes(node.left, prefix + '0', codebook)
            HEAPQ.generate_codes(node.right, prefix + '1', codebook)

        return codebook

    @staticmethod
    def compress_file(input_file, output_file):
        with open(input_file, 'rb') as file:
            data = file.read()

        # Строим дерево Хаффмана и получаем коды
        tree = HEAPQ.build_huffman_tree(data)
        codes = HEAPQ.generate_codes(tree)

        # Сжимаем данные
        compressed_data = ''.join(codes[byte] for byte in data)

        # Сохраняем сжатые данные и кодировку
        with open(output_file, 'wb') as file:
            # Сохраняем длину оригинальных данных для восстановления
            file.write(len(data).to_bytes(8, byteorder='big'))

            # Сохраняем коды в бинарном формате
            for byte, code in codes.items():
                byte_value = bytes([byte])
                file.write(byte_value)  # Записываем байт
                file.write(len(code).to_bytes(1, byteorder='big'))  # Длина кода
                file.write(int(code, 2).to_bytes((len(code) + 7) // 8, byteorder='big'))  # Сам код

            # Сохраняем сжатые данные
            byte_data = [int(compressed_data[i:i+8], 2) for i in range(0, len(compressed_data), 8)]
            file.write(bytes(byte_data))

    @staticmethod
    def decompress_file(input_file, output_file):
        with open(input_file, 'rb') as file:
            # Читаем длину исходных данных
            original_length = int.from_bytes(file.read(8), byteorder='big')

            # Читаем коды Хаффмана
            codes = {}
            while True:
                byte = file.read(1)
                if not byte:
                    break
                byte = byte[0]

                # Читаем длину кода
                code_length = int.from_bytes(file.read(1), byteorder='big')

                # Читаем сам код
                code_value = int.from_bytes(file.read((code_length + 7) // 8), byteorder='big')
                code = bin(code_value)[2:].zfill(code_length)

                codes[code] = byte

            # Читаем сжатые данные
            compressed_data = ''
            byte = file.read(1)
            while byte:
                compressed_data += bin(byte[0])[2:].zfill(8)
                byte = file.read(1)

            # Восстанавливаем оригинальные данные
            buffer = ''
            decompressed_data = []
            for bit in compressed_data:
                buffer += bit
                if buffer in codes:
                    decompressed_data.append(codes[buffer])
                    buffer = ''

            # Записываем восстановленные данные
            with open(output_file, 'wb') as file:
                file.write(bytes(decompressed_data[:original_length]))