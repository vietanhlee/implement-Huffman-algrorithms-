import heapq
from collections import defaultdict

# Định nghĩa 1 node
class HuffmanNode:
    def __init__(self, freq, byte=None, left=None, right=None):
        self.freq = freq # Tần số
        self.byte = byte # Giá trị byte của node (chỉ các node lá mới có giá trị này) (mặc định sẽ là None nếu ko truyền tham số)
        self.left = left # Node trái
        self.right = right # Node phải

    # Định nghĩa thuộc tính này phục vụ cho việc so sánh trong pq
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    def __init__(self):
        # Dict tra code nén 
        """
        codes = {
                bytes: code
            }
            
            reverse_mapping thì ngược lại
        """
        self.codes = {}
        # Dict tra code giải nén
        self.reverse_mapping = {}

    def build_frequency_dict(self, data_bytes : list) -> dict:
        """Tạo tần số theo bytes"""
        freq = defaultdict(int)
        for b in data_bytes:
            freq[b] += 1
        return freq
 
    def build_heap(self, freq_dict : dict) -> list[HuffmanNode]:
        """Build priority queue chứa các node"""
        heap = []
        for byte, frequency in freq_dict.items():
            # Tạo các node lá (chứa các byte)
            node = HuffmanNode(frequency, byte)            
            heapq.heappush(heap, node)
        return heap

    def merge_nodes_huffman(self, heap : list[HuffmanNode]) -> list:
        """Gộp từng 2 node nhỏ nhất lại thành 1 """
        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)
            
            # Node nhỏ bên trái node lớn hơn bên phải
            merged = HuffmanNode(node1.freq + node2.freq, left=node1, right=node2)
            # Đưa vào pq
            heapq.heappush(heap, merged)
        return heap

    def func_make_code_from_node(self, node : HuffmanNode, current_code: str) -> None:
        """Tạo code cho các node từ một node start"""
        # Điều kiện dừng nếu node truyền vào là None
        if node is None:
            return
        
        # Điều kiện dừng khi gặp node lá tức bytes ban đầu ta cần    
        if node.byte is not None:
            self.codes[node.byte] = current_code
            self.reverse_mapping[current_code] = node.byte
            return
        
        # Gọi đệ quy đến 2 nhánh sau
        self.func_make_code_from_node(node.left, current_code + "0")
        self.func_make_code_from_node(node.right, current_code + "1")

    def make_codes_huffman_from_root(self, heap : HuffmanNode) -> None:
        """Tạo mã huffman từ root đầu vào là pq chứa 1 huffmannode duy nhất

Gọi hàm này sau khi gộp hết các node huffman"""
        root = heapq.heappop(heap)
        self.func_make_code_from_node(root, "")

    def get_encoded_data(self, data_bytes : list) -> str:
        """Mã hoá data
        
Đầu ra 8 bit đầu chứa số bit padding"""
        encoded_bits = "".join(self.codes[bytes] for bytes in data_bytes)
        extra_padding = 8 - len(encoded_bits) % 8
        encoded_bits += "0" * extra_padding
        padded_info = f"{extra_padding:08b}"
        
        return padded_info + encoded_bits

    def get_byte_array(self, padded_encoded_bits : str) -> bytearray:
        return bytearray(int(padded_encoded_bits[i:i+8], 2) for i in range(0, len(padded_encoded_bits), 8))

    def compress(self, input_path : str, output_path : str):
        # output_path =  'out_' + input_path.split('.')[0] + '.bin'
        with open(input_path, 'rb') as file:
            data = file.read()

        print('Đã đọc xong file')
        
        # Các thủ tục tạo data
        freq_dict = self.build_frequency_dict(data)
        heap = self.build_heap(freq_dict)
        heap = self.merge_nodes_huffman(heap)
        # Lấy data cho 2 dict code và mapping_reverse
        self.make_codes_huffman_from_root(list(heap))

        print('Đã tạo xong code')
        
        # Tạo bytes array chứa data (1 byte = 8 bit)
        padded_encoded_bits = self.get_encoded_data(data)
        b_arr = self.get_byte_array(padded_encoded_bits)

        with open(output_path, 'wb') as output:
            mapping_size = len(self.codes)
            output.write(mapping_size.to_bytes(2, 'big'))
            
            # Ghi thông tin bảng mã nén  Byte gốc	Độ dài mã	Mã code mã hoá dạng byte
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
