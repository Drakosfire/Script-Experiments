from docling.document_converter import DocumentConverter

source = "./PHB2024.pdf"  # PDF path or URL
converter = DocumentConverter()
result = converter.convert_single(source)
print(result.render_as_markdown())  # output: "## Docling Technical Report[...]"
print(result.render_as_doctags())  # output: "<document><title><page_1><loc_20>..."