from docx_parser_converter import DocumentConverter

# Paths to your input .docx and output HTML files
docx_path = "/home/x2p/Downloads/التزامات/"
html_path = "output.html"

# Create a converter instance and perform the conversion
converter = DocumentConverter()
converter.convert_to_html(docx_path, html_path)

print(f"Conversion complete! HTML saved as {html_path}")