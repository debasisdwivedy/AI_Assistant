import os,sys
sys.path.append(os.getcwd())

from langchain_core.prompts import PromptTemplate
from Prompts import Prompts

from unstructured.partition.common import UnsupportedFileFormatError
from utils.get_llm import get_llm
from utils.get_embeddings import get_embedding
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage, AnyMessage
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter,TokenTextSplitter, RecursiveCharacterTextSplitter,SpacyTextSplitter
from langchain_chroma import Chroma

def read_file(file_path:str,query:str=None)->str:
    """
    Tool: File reader to read files of ANY TYPE

        Name : read_file

        Description:
            This tool is used to read files of different format.
            The result return is of type string

        Args:
            file_path:str = The name/path/url of the file to be read.
            query:str = Question that needs to be answer from the file.Make the query EXTREMLY DETAILED, SELF EXPLANATORY and WITHOUT AMBIGUITY.

        Usage:
            Call this tool if you want to read a file present in local or a URL to the file.

        Output:

            result:str = The result from the function call
    """
    filename=file_path
    root, ext = os.path.splitext(filename)
    text_extensions = [".py",".c",".java",".cs",".php",".swift",".vb",".sql",".html",".htm",".txt",".md",".pdb"]
    image_extension = [".jpeg",".jpg",".png",".gif",".svg",".bmp",".webp",".tiff",".tif"]

    if file_path.startswith("http"):
        import requests
        response = requests.get(file_path)
        response.raise_for_status
        content = response.content
        filename=__download_file__(content)
    
    if ext in text_extensions:
        with open(f"tools/file_ops/temp/{filename}","r") as f:
            content = f.read()
        #print(content)
        if len(content) > 10000 and ext in [".html",".htm",".txt",".md",".pdb"]:
            return __most_relevant_sections__(content,query)
        else:
            return content
    elif ext in image_extension:
        # Load image and convert to base64
        import base64
        with open(f"tools/file_ops/temp/{filename}", "rb") as img:
            base64_image = base64.b64encode(img.read()).decode("utf-8")

        prompt_template = PromptTemplate.from_template(Prompts.READ_IMAGE_PROMPT.value)
        prompt = prompt_template.invoke({
            "question": query
        })
        
        messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": str(prompt)},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
            ],
        }
    ]
        llm = get_llm()
        resp = llm.invoke(messages)
        return resp.content
    else:
        loader = __load_file__(filename)
        content = []
        if loader:
            try:
                elements = loader.partition()
                #print(len(elements))
                for element in elements:
                    # print(element.id)
                    # print(element.category)
                    # print(element.metadata)
                    # print(element.text)
                    #break
                    content.append(element.text)
            except Exception as e:
                print(f"Unable to partition file {filename} using Unstructured!!!")
        s = " ".join(content)
        #print(s)
        if len(s) < 10000:
            return s
        else:
            return __most_relevant_sections__(content,query)
    

def __get_file_type_from_binary__(binary_data):
    import magic
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
            try:
                from tools.file_ops.readers.pdf_loader import pdf_loader
                loader = pdf_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".doc":
            try:
                from tools.file_ops.readers.doc_loader import doc_loader
                loader = doc_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".docx":
            try:
                from tools.file_ops.readers.docx_loader import docx_loader
                loader = docx_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".eml":
            try:
                from tools.file_ops.readers.email_loader import email_loader
                loader = email_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".epub":
            try:
                from tools.file_ops.readers.epub_loader import epub_loader
                loader = epub_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".xls":
            try:
                from tools.file_ops.readers.excel_loader import excel_loader
                loader = excel_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".xlsx":
            try:
                from tools.file_ops.readers.excel_loader import excel_loader
                loader = excel_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".msg":
            try:
                from tools.file_ops.readers.message_loader import message_loader
                loader = message_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".odt":
            try:
                from tools.file_ops.readers.open_office_loader import open_office_loader
                loader = open_office_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".ppt":
            try:
                from tools.file_ops.readers.ppt_loader import ppt_loader
                loader = ppt_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".pptx":
            try:
                from tools.file_ops.readers.pptx_loader import pptx_loader
                loader = pptx_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".rtf":
            try:
                from tools.file_ops.readers.rtf_loader import rtf_loader
                loader = rtf_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".xml":
            try:
                from tools.file_ops.readers.xml_loader import xml_loader
                loader = xml_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".html":
            try:
                from tools.file_ops.readers.html_loader import html_loader
                loader = html_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".jpeg" | ".jpg" | ".png" | ".gif" | ".svg" | ".bmp" | ".webp" | ".tiff" | ".tif":
            try:
                from tools.file_ops.readers.image_loader import image_loader
                loader = image_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".csv":
            try:
                from tools.file_ops.readers.csv_loader import csv_loader
                loader = csv_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        # case ".txt":
        #     try:
        #         from tools.file_ops.readers.text_loader import text_loader
        #         loader = text_loader(f"tools/file_ops/temp/{filename}")
        #     except Exception as e:
        #         print(f"Unable to read the file {filename}")

        case ".md":
            try:
                from tools.file_ops.readers.markdown_loader import markdown_loader
                loader = markdown_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".rst":
            try:
                from tools.file_ops.readers.rst_loader import rst_loader
                loader = rst_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".org":
            try:
                from tools.file_ops.readers.org_loader import org_loader
                loader = org_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case ".tsv":
            try:
                from tools.file_ops.readers.tsv_loader import tsv_loader
                loader = tsv_loader(f"tools/file_ops/temp/{filename}")
            except Exception as e:
                print(f"Unable to read the file {filename}")

        case _:
            try:
                from tools.file_ops.readers.anonymous_file_loader import anonymous_file_loader
                loader = anonymous_file_loader(f"tools/file_ops/temp/{filename}")
            except UnsupportedFileFormatError as e:
                print(f"Unable to read the file {filename}")

    return loader

def __most_relevant_sections__(content:str,query:str,k:int=5,content_max_size:int=1000000):
    print("=============================VECTOR SERACH FOR LARGE FILE=========================")
    most_relevant_content =[]

    # Split into chunks
    text_splitter = CharacterTextSplitter(chunk_size=5000, chunk_overlap=100)
    token_splitter =  TokenTextSplitter(chunk_size=5000, chunk_overlap=100)
    recursive_text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=100)
    spacy_text_splitter = SpacyTextSplitter(pipeline="en_core_web_sm", chunk_size=5000, chunk_overlap=100)


    texts = token_splitter.split_text(content[:content_max_size])

    # Create embedding model
    embedding = get_embedding()

    # Create Chroma DB from documents
    vectorstore = Chroma.from_texts(texts, embedding)

    # Perform similarity search
    results = vectorstore.similarity_search(query, k=k)
    for result in results:
        # print("++++++++++++++++++++++++++++++++++++++++++++")
        # print(result.page_content)
        # print("++++++++++++++++++++++++++++++++++++++++++++")
        most_relevant_content.append(result.page_content)
    
    #print("\n\n".join(most_relevant_content))
    print("======================================================")
    return "\n\n".join(most_relevant_content)

if __name__ == "__main__":
    # Dataset_Philosophy_Ethics_Morality.csv
    # 1745745409584.pdf - ISSUE (NUMPY)
    # 2501.19393v3.pdf - ISSUE (NUMPY)
    # Prudential_OTP_demo_Results.xlsx
    # Hugging _Face_Certificate.webp
    # 1707100541036.jpeg - ISSUE (NUMPY)
    # Best_of_Bali_2023.pptx

    read_file("Sherlock_Holmes_Canon.txt","Who was sherlock holmes best friend?")