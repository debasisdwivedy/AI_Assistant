from unstructured.partition.html import partition_html

class html_loader():
    def __init__(self,input_file_path)->None:
        self.input_file_path=input_file_path
        self.extract_images_in_pdf= True
        self.infer_table_structure= True
        self.chunking_strategy= "by_title"
        self.max_characters= 30000
        self.extract_image_block_types= ["Image", "Table"]
        self.extract_image_block_to_payload= True
        self.skip_headers_and_footers= True
        self.ssl_verify= False
        self.encoding= None
        self.include_page_breaks= False
        self.include_metadata= True
        self.headers= {}
        self.parser= None
        self.source_format= None
        self.html_assemble_articles= False
        self.metadata_filename= None
        self.metadata_last_modified= None
        self.languages= None
        self.detect_language_per_element= False
        self.detection_origin= False
        self.date_from_file_object= False
        
    def partition(self):
        elements = elements = partition_html(url=self.input_file_path,
                                            extract_images_in_pdf=self.extract_images_in_pdf,
                                            infer_table_structure=self.infer_table_structure,
                                            chunking_strategy=self.chunking_strategy,
                                            max_characters=self.max_characters,
                                            extract_image_block_types=self.extract_image_block_types,
                                            extract_image_block_to_payload=self.extract_image_block_to_payload,
                                            skip_headers_and_footers=self.skip_headers_and_footers,
                                            ssl_verify=self.ssl_verify,
                                            encoding=self.encoding,
                                            include_page_breaks=self.include_page_breaks,
                                            include_metadata=self.include_metadata,
                                            headers=self.headers,
                                            parser=self.parser,
                                            source_format=self.source_format,
                                            html_assemble_articles=self.html_assemble_articles,
                                            metadata_filename=self.metadata_filename,
                                            metadata_last_modified=self.metadata_last_modified,
                                            languages=self.languages,
                                            detect_language_per_element=self.detect_language_per_element,
                                            detection_origin=self.detection_origin,
                                            date_from_file_object=self.date_from_file_object,
                                            )
        return elements