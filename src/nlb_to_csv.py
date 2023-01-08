import sys
from pdfminer.high_level import extract_text
from conf import INPUT_DIR
from src import parser

def main():
    if (args_count := len(sys.argv)) > 3:
        print(f"Two arguments expected, got {args_count - 1}")
        raise SystemExit(2)
        
    text = extract_text(INPUT_DIR + sys.argv[1])
    parser(text).to_csv(name=sys.argv[2])


if __name__ == "__main__":
    main()

