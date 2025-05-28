# Project: brief description about project
# To fulfil the requirement of FIT Course by Pham@PTIT
# LE VIET ANH - B23DCKH002 - 13
# LE VAN THANH - B23DCKH109- 14
# NGUYEN VAN LONG - B23DCKH072 - 13
# DO TRAN HIEU - B23DCKH038 - 13

from huffman import HuffmanCoding
import sys
import argparse

if __name__ == "__main__":
    h = HuffmanCoding()
    
    parser = argparse.ArgumentParser()
    
    
    parser.add_argument("--mode", type=int, choices=[0, 1], required=True,
                    help="0 for compress, 1 for decompress")
    parser.add_argument("--input",type= str, required= True, help= "name of file input")
    parser.add_argument("--output",type= str, required= True, help= "output file of file output")  

    
    args = parser.parse_args()
    
    if args.mode == 0:
        h.compress(args.input, args.output)
    else:
        h.decompress(args.input, args.output)

