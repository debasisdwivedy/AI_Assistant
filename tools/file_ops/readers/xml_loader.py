from unstructured.partition.xml import partition_xml
class xml_loader:
    def __init__(self,input_file_path)->None:
        self.input_file_path=input_file_path
        self.extract_images_in_pdf= True
        self.infer_table_structure= True
        self.chunking_strategy= "by_title"
        self.strategy= "hi_res"
        self.max_characters= 30000
        self.extract_image_block_types= ["Image", "Table"]
        self.extract_image_block_to_payload= True
        self.include_page_breaks= False
        self.languages= None
        self.include_metadata= True
        self.metadata_filename= None
        self.metadata_last_modified= None
        self.links= []
        self.hi_res_model_name= None
        self.extract_image_block_output_dir= None
        self.date_from_file_object= False
        
    def partition(self):
        elements = partition_xml(self.input_file_path,
                                 extract_images_in_pdf=self.extract_images_in_pdf,
                                infer_table_structure=self.infer_table_structure,
                                chunking_strategy=self.chunking_strategy,
                                strategy=self.strategy,
                                max_characters=self.max_characters,
                                extract_image_block_types=self.extract_image_block_types,
                                extract_image_block_to_payload=self.extract_image_block_to_payload,
                                include_page_breaks=self.include_page_breaks,
                                languages=self.languages,
                                include_metadata=self.include_metadata,
                                metadata_filename=self.metadata_filename,
                                metadata_last_modified=self.metadata_last_modified,
                                links=self.links,
                                hi_res_model_name=self.hi_res_model_name,
                                extract_image_block_output_dir=self.extract_image_block_output_dir,
                                date_from_file_object=self.date_from_file_object)
        return elements
