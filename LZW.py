class LZW:
    @staticmethod
    def _compress(data):
        # Инициализация словаря с начальными символами (байтами от 0 до 255)
        dictionary_size = 256
        dictionary = {bytes([i]): i for i in range(dictionary_size)}
        current_bytes = bytes()
        compressed_data = []

        # Проход по каждому байту входных данных
        for byte in data:
            combined_bytes = current_bytes + bytes([byte])
            if combined_bytes in dictionary:
                # Если комбинация уже есть в словаре, обновляем текущие байты
                current_bytes = combined_bytes
            else:
                # Если комбинации нет в словаре, добавляем текущие байты в сжатые данные
                compressed_data.append(dictionary[current_bytes])
                # Добавляем новую комбинацию в словарь
                dictionary[combined_bytes] = dictionary_size
                dictionary_size += 1
                # Обновляем текущие байты
                current_bytes = bytes([byte])

        # Добавление оставшихся данных в сжатый список
        if current_bytes:
            compressed_data.append(dictionary[current_bytes])

        return compressed_data

    @staticmethod
    def _decompress(compressed_data):
        # Инициализация словаря с начальными символами (байтами от 0 до 255)
        dictionary_size = 256
        dictionary = {i: bytes([i]) for i in range(dictionary_size)}
        # Извлекаем первый код и преобразуем его в байты
        current_bytes = bytes([compressed_data.pop(0)])
        decompressed_data = bytearray(current_bytes)

        # Проход по каждому коду в сжатых данных
        for code in compressed_data:
            if code in dictionary:
                entry = dictionary[code]
            elif code == dictionary_size:
                # Специальный случай для кода, равного размеру словаря
                entry = current_bytes + current_bytes[:1]
            else:
                raise ValueError("Ошибка в сжатых данных: неверный код.")

            # Добавляем восстановленные байты в итоговый массив
            decompressed_data.extend(entry)
            # Добавляем новую комбинацию в словарь
            dictionary[dictionary_size] = current_bytes + entry[:1]
            dictionary_size += 1
            # Обновляем текущие байты
            current_bytes = entry

        return decompressed_data

    @staticmethod
    def compress_file(input_file_path, output_file_path):
        with open(input_file_path, 'rb') as input_file:
            data = input_file.read()
            compressed_data = LZW._compress(data)

            with open(output_file_path, 'wb') as output_file:
                for code in compressed_data:
                    # Записываем каждый код в виде 3 байтов
                    output_file.write(code.to_bytes(3, 'big'))

    @staticmethod
    def decompress_file(input_file_path, output_file_path):
        with open(input_file_path, 'rb') as input_file:
            compressed_data = []
            while True:
                # Читаем 3 байта за раз
                bytes_read = input_file.read(3)
                if not bytes_read:
                    break
                # Преобразуем 3 байта в целое число
                compressed_data.append(int.from_bytes(bytes_read, 'big'))

            data = LZW._decompress(compressed_data)

            with open(output_file_path, 'wb') as output_file:
                output_file.write(data)