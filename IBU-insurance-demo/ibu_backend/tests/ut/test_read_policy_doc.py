import sys, os
from docx import Document

file_path = "../scenarios/IBU_policies_2.docx"
doc = Document(file_path)
fullText = []
for para in doc.paragraphs:
    fullText.append(para.text)
txt='\n'.join(fullText)
print(txt)