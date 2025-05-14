import heapq
from collections import defaultdict

# Định nghĩa 1 node
class HuffmanNode:
    def __init__(self, freq, byte=None, left=None, right=None):
        self.freq = freq # Tần số
        self.byte = byte # Giá trị byte của node (chỉ các node lá mới có giá trị này) (mặc định sẽ là None nếu ko truyền tham số)
        self.left = left # Node trái
        self.right = right # Node phải

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    def __init__(self):
        self.codes = {}
        self.reverse_mapping = {}

    # Tạo tần số 
    def build_frequency_dict(self, data_bytes):
        freq = defaultdict(int)
        for b in data_bytes:
            freq[b] += 1
        return freq

    # Build priority queue chứa các node 
    def build_heap(self, freq_dict):
        heap = []
        for byte, frequency in freq_dict.items():
            # Tạo các node lá (chứa các byte)
            node = HuffmanNode(frequency, byte)            
            heapq.heappush(heap, node)
        return heap

    # Gộp từng node nhỏ nhất lại thành 1 
    def merge_nodes(self, heap):
        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)
            
            # Node nhỏ bên trái node lớn hơn bên phải
            merged = HuffmanNode(node1.freq + node2.freq, left=node1, right=node2)
            heapq.heappush(heap, merged)
        return heap

    # Tạo chỉ số các nhánh    
    def make_codes_helper(self, node, current_code):
        # Điều kiện dừng nếu node truyền vào là None
        if node is None:
            return
        
        # Điều kiện dừng khi gặp node lá    
        if node.byte is not None:
            self.codes[node.byte] = current_code
            self.reverse_mapping[current_code] = node.byte
            return
        
        # Gọi đệ quy
        self.make_codes_helper(node.left, current_code + "0")
        self.make_codes_helper(node.right, current_code + "1")

    # Lệnh gọi tạo các mã huffman
    def make_codes(self, heap):
        root = heapq.heappop(heap)
        self.make_codes_helper(root, "")

    
    def get_encoded_data(self, data_bytes):
        encoded_bits = "".join(self.codes[b] for b in data_bytes)
        extra_padding = 8 - len(encoded_bits) % 8
        encoded_bits += "0" * extra_padding
        padded_info = f"{extra_padding:08b}"
        return padded_info + encoded_bits

    def get_byte_array(self, padded_encoded_bits):
        if len(padded_encoded_bits) % 8 != 0:
            raise ValueError("Encoded bits length is not padded to full bytes.")
        return bytearray(int(padded_encoded_bits[i:i+8], 2) for i in range(0, len(padded_encoded_bits), 8))

    def compress(self, input_path : str, output_path : str):
        # output_path =  'out_' + input_path.split('.')[0] + '.bin'
        with open(input_path, 'rb') as file:
            data = file.read()

        print('Đã đọc xong file')
        
        freq_dict = self.build_frequency_dict(data)
        heap = self.build_heap(freq_dict)
        heap = self.merge_nodes(heap)
        self.make_codes(list(heap))

        print('Đã tạo xong code')
        
        padded_encoded_bits = self.get_encoded_data(data)
        b_arr = self.get_byte_array(padded_encoded_bits)

        with open(output_path, 'wb') as output:
            # Ghi thông tin bảng mã nén
            mapping_size = len(self.codes)
            output.write(mapping_size.to_bytes(2, 'big'))
            for byte, code in self.codes.items():
                output.write(bytes([byte]))
                code_length = len(code)
                output.write(bytes([code_length]))
                output.write(int(code, 2).to_bytes((code_length + 7) // 8, 'big'))
            
            # Ghi mã nén
            output.write(b_arr)

        print(f"Nén thành công file {input_path} vào file {output_path}")

    def remove_padding(self, padded_encoded_bits):
        padded_info = padded_encoded_bits[:8]
        extra_padding = int(padded_info, 2)
        padded_encoded_bits = padded_encoded_bits[8:]
        if extra_padding:
            return padded_encoded_bits[:-extra_padding]
        return padded_encoded_bits

    def decompress(self, input_path, output_path):
        with open(input_path, 'rb') as file:
            bit_data = file.read()

        # output_path = 'out_' + input_path[:-3] + type_of_file_output
        mapping_size = int.from_bytes(bit_data[:2], 'big')
        print('Đã đọc xong thông tin bảng mã')
        idx = 2
        
        self.codes.clear()
        self.reverse_mapping.clear()
        
        for _ in range(mapping_size):
            byte = bit_data[idx]
            idx += 1
            
            code_length = bit_data[idx]
            idx += 1
            
            num_bytes = (code_length + 7) // 8
            code_bytes = bit_data[idx : idx + num_bytes]
                        
            idx += num_bytes
            
            code_int = int.from_bytes(code_bytes, 'big')
            code = f"{code_int:0{code_length}b}"
            
            self.codes[byte] = code
            self.reverse_mapping[code] = byte

        # Phần dữ liệu nén
        encoded_bytes = bit_data[idx:] 
        bit_string = "".join(f"{b:08b}" for b in encoded_bytes)
        actual_bits = self.remove_padding(bit_string)

        # Mã hiện tại (biến khởi tạo)
        current_code = ""
        # Mã sau giải nén
        decoded_bytes = bytearray()
        # Lặp qua từng bit một
        for bit in actual_bits:
            # Thêm vào mã hiện tại
            current_code += bit
            # Nếu mã hiện tại có trong bộ mã đict thì thêm vào Mã sau giải nén
            if current_code in self.reverse_mapping:
                decoded_bytes.append(self.reverse_mapping[current_code])
                current_code = ""

        # Ghi kết quả
        with open(output_path, 'wb') as output:
            output.write(decoded_bytes)

        print(f"Giải nén đã xong file {input_path} vào file {output_path}")
