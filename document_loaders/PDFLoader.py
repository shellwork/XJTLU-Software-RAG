from langchain.document_loaders import PyPDFLoader

loader=PyPDFLoader("...")  #replace ... with indicated file path
pages_pypdf_image=loader.load()

len(pages_pypdf_image)  #print page number of pdf document
print(pages_pypdf_image[*].page_content)  #replace * with indicated page number
                                          #image content printed below text content
print(len(pages_pypdf_image[*].page_content))  #replace * with indicated page number
                                               #print string number of the indicated page
pages_pypdf_image[*].page_content[a:b]  #replace * with indicated page number, replace a&b with indicated string number
                                        #print content between string number a and b
