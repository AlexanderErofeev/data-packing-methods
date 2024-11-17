import os
from HEAPQ import HEAPQ
from LZW import LZW
from MTF import MTF

def calculate_compression_degree(input_file_path: str, output_file_path: str) -> None:
    input_file_size = os.path.getsize(input_file_path)
    print(f"Объём исходного файла: {input_file_size} байт")
    output_file_size = os.path.getsize(output_file_path)
    print(f"Объём сжатого файла: {output_file_size} байт")
    print(f"Коэффициент сжатия: {input_file_size / output_file_size}")
    print(f"Степень сжатия: {(input_file_size - output_file_size) / input_file_size}")


input_file = "data/2023-12-04 15-25-42.mkv"
temp_file = input_file + "_temp.dat"
compressed_file = input_file + "_compressed.dat"
decompressed_file = input_file + "_decompressed.dat"

print("Тестирование LZW сжатия")
LZW.compress_file(input_file, compressed_file)
calculate_compression_degree(input_file, compressed_file)
print("_______________________")

print("Тестирование HEAPQ сжатия")
HEAPQ.compress_file(input_file, compressed_file)
calculate_compression_degree(input_file, compressed_file)
print("_______________________")

print("Тестирование LZW сжатия, после предобработки MTF")
MTF.compress_file(input_file, temp_file)
LZW.compress_file(temp_file, compressed_file)
calculate_compression_degree(input_file, compressed_file)
print("_______________________")

print("Тестирование HEAPQ сжатия, после предобработки MTF")
MTF.compress_file(input_file, temp_file)
HEAPQ.compress_file(temp_file, compressed_file)
calculate_compression_degree(input_file, compressed_file)
print("_______________________")
