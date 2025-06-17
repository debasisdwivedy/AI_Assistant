def read_file(file_path:str)->str:
    filename=file_path
    if file_path.startswith("http"):
        import requests
        response = requests.get(file_path)
        response.raise_for_status
        content = response.content
        filename=__download_file__(content)
    
    # loader = __load_file__(filename)
    # elements = loader.partition()
    # for element in elements:
    #     print(element.id)
    #     print(element.category)
    #     print(element.metadata)
    #     print(element.text)
    #     break
    

def __get_file_type_from_binary__(binary_data):
    import pylibmagic, magic
    mime = magic.Magic(mime=True)  # Get MIME type
    file_type = mime.from_buffer(binary_data)
    return file_type

def __download_file__(content)->str:
    import uuid
    file_type = __get_file_type_from_binary__(content)
    print(file_type)
    ext="unknown"
    uid = str(uuid.uuid4())
    match file_type:
        case "application/pdf":
            ext="pdf"
            print("PDF")
        case "application/msword":
            ext="doc"
            print("DOC")
        case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            ext="docx"
            print("DOCX")
        case "message/rfc822":
            ext="eml"
            print("EML")
        case "application/epub+zip":
            ext="epub"
            print("EPUB")
        case "application/vnd.ms-excel":
            ext="xls"
            print("EXCEL->XLS")
        case "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            ext="xlsx"
            print("EXCEL->XLSX")
        case "application/vnd.ms-outlook":
            ext="msg"
            print("MSG")
        case "application/vnd.oasis.opendocument.text":
            ext="odt"
            print("ODT")
        case "application/application/vnd.ms-powerpoint":
            ext="ppt"
            print("PPT")
        case "application/vnd.openxmlformats-officedocument.presentationml.presentation":
            ext="pptx"
            print("PPTX")
        case "application/rtf":
            ext="rtf"
            print("RTF")
        case "application/XML":
            ext="xml"
            print("XML")
        case "text/html":
            ext="html"
            print("HTML")
        case "image/jpeg":
            ext="jpeg"
            print("JPEG")
        case "image/png":
            ext="png"
            print("PNG")
        case "image/gif":
            ext="gif"
            print("GIF")
        case "image/svg+xml":
            ext="svg"
            print("SVG")
        case "image/bmp":
            ext="bmp"
            print("BMP")
        case "image/webp":
            ext="webp"
            print("WEBP")
        case "image/tiff":
            ext="tiff"
            print("TIFF")
        case "text/csv":
            ext="csv"
            print("CSV")
        case "text/plain":
            ext="txt"
            print("TXT")
        case "text/markdown":
            ext="md"
            print("MARKDOWN")
        case "text/x-rst":
            ext="rst"
            print("RST")
        case "text/tab-separated-values":
            ext="tsv"
            print("TSV")
        case _:
            ext="unknown"
            print("remaining")

    with open(f"tools/file_ops/temp/{uid}.{ext}", 'wb') as file:
        file.write(content)
        print("File downloaded successfully")
    
    return f"{uid}.{ext}"

def __load_file__(filename):
    import os
    root, ext = os.path.splitext(filename)
    ext_lower = ext.lower()
    match ext_lower:
        case ".pdf":
            from readers.pdf_loader import pdf_loader
            loader = pdf_loader(f"tools/file_ops/temp/{filename}")
        case ".doc":
            from readers.doc_loader import doc_loader
            loader = doc_loader(f"tools/file_ops/temp/{filename}")
        case ".docx":
            from readers.docx_loader import docx_loader
            loader = docx_loader(f"tools/file_ops/temp/{filename}")
        case ".eml":
            from readers.email_loader import email_loader
            loader = email_loader(f"tools/file_ops/temp/{filename}")
        case ".epub":
            from readers.epub_loader import epub_loader
            loader = epub_loader(f"tools/file_ops/temp/{filename}")
        case ".xls":
            from readers.excel_loader import excel_loader
            loader = excel_loader(f"tools/file_ops/temp/{filename}")
        case ".xlsx":
            from readers.excel_loader import excel_loader
            loader = excel_loader(f"tools/file_ops/temp/{filename}")
        case ".msg":
            from readers.message_loader import message_loader
            loader = message_loader(f"tools/file_ops/temp/{filename}")
        case ".odt":
            from readers.open_office_loader import open_office_loader
            loader = open_office_loader(f"tools/file_ops/temp/{filename}")
        case ".ppt":
            from readers.ppt_loader import ppt_loader
            loader = ppt_loader(f"tools/file_ops/temp/{filename}")
        case ".pptx":
            from readers.pptx_loader import pptx_loader
            loader = pptx_loader(f"tools/file_ops/temp/{filename}")
        case ".rtf":
            from readers.rtf_loader import rtf_loader
            loader = rtf_loader(f"tools/file_ops/temp/{filename}")
        case ".xml":
            from readers.xml_loader import xml_loader
            loader = xml_loader(f"tools/file_ops/temp/{filename}")
        case ".html":
            from readers.html_loader import html_loader
            loader = html_loader(f"tools/file_ops/temp/{filename}")
        case ".jpeg" | ".jpg" | ".png" | ".gif" | ".svg" | ".bmp" | ".webp" | ".tiff" | ".tif":
            from readers.image_loader import image_loader
            loader = image_loader(f"tools/file_ops/temp/{filename}")
        case ".csv":
            from readers.csv_loader import csv_loader
            loader = csv_loader(f"tools/file_ops/temp/{filename}")
        case ".txt":
            from readers.text_loader import text_loader
            loader = text_loader(f"tools/file_ops/temp/{filename}")
        case ".md":
            from readers.markdown_loader import markdown_loader
            loader = markdown_loader(f"tools/file_ops/temp/{filename}")
        case ".rst":
            from readers.rst_loader import rst_loader
            loader = rst_loader(f"tools/file_ops/temp/{filename}")
        case ".org":
            from readers.org_loader import org_loader
            loader = org_loader(f"tools/file_ops/temp/{filename}")
        case ".tsv":
            from readers.tsv_loader import tsv_loader
            loader = tsv_loader(f"tools/file_ops/temp/{filename}")
        case _:
            from readers.anonymous_file_loader import anonymous_file_loader
            loader = anonymous_file_loader(f"tools/file_ops/temp/{filename}")

    return loader




# Dataset_Philosophy_Ethics_Morality.csv
# 1745745409584.pdf - ISSUE (NUMPY)
# 2501.19393v3.pdf - ISSUE (NUMPY)
# Prudential_OTP_demo_Results.xlsx
# Hugging _Face_Certificate.webp
# 1707100541036.jpeg - ISSUE (NUMPY)
# Best_of_Bali_2023.pptx

read_file("")