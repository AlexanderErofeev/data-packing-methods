class MTF:
    @staticmethod
    def _encode(data):
        symbols = list(set(data))
        mtf = []
        for char in data:
            index = symbols.index(char)
            mtf.append(index)
            symbols.pop(index)
            symbols.insert(0, char)
        return mtf, symbols

    @staticmethod
    def _decode(mtf, symbols):
        data = []
        for index in mtf:
            char = symbols[index]
            data.append(char)
            symbols.pop(index)
            symbols.insert(0, char)
        return bytes(data)

    @staticmethod
    def compress_file(input_file, output_file):
        with open(input_file, 'rb') as f:
            data = f.read()

        mtf, symbols = MTF._encode(data)

        with open(output_file, 'wb') as f:
            f.write(len(symbols).to_bytes(2, 'big'))
            f.write(bytes(symbols))
            f.write(bytes(mtf))

    @staticmethod
    def decompress_file(input_file, output_file):
        with open(input_file, 'rb') as f:
            num_symbols = int.from_bytes(f.read(2), 'big')
            symbols = list(f.read(num_symbols))
            mtf = list(f.read())

        data = MTF._decode(mtf, symbols)

        with open(output_file, 'wb') as f:
            f.write(data)