import os
import argparse
import PyPDF2


def parse_pdf(filepath, outpath):
    with open(filepath, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page_text = reader.pages[page_num].extract_text() or ''
            text += page_text + '\n'
    os.makedirs(os.path.dirname(outpath) or '.', exist_ok=True)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(text)


def main():
    parser = argparse.ArgumentParser(description='Parse PDF files to plain text/markdown')
    parser.add_argument('input', help='PDF file path')
    parser.add_argument('output', help='Output markdown path')
    args = parser.parse_args()
    parse_pdf(args.input, args.output)


if __name__ == '__main__':
    main()
