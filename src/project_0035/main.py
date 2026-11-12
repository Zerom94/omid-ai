import argparse
from qr_generator import generate_qr

def main():
    parser = argparse.ArgumentParser(description="Generate QR code from input text.")
    parser.add_argument("data", help="Text or URL to encode")
    parser.add_argument("-o", "--output", default="qr.png", help="Output image file")
    parser.add_argument("-s", "--size", type=int, default=10, help="Box size (pixel size of each box)")
    parser.add_argument("-b", "--border", type=int, default=4, help="Border size (boxes)")
    args = parser.parse_args()
    img = generate_qr(args.data, box_size=args.size, border=args.border)
    img.save(args.output)
    print(f"QR code saved to {args.output}")

if __name__ == "__main__":
    main()
