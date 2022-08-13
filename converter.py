from pandas import read_excel
from docx import Document
import pdfminer.high_level
import os
from pathlib import Path
import comparator
from datetime import datetime
import temp_data

def CMP(source_dir:str,log_func):
    try:
        log_func("Сканирование файлов...")
        
        texts = {}
        filenames = os.listdir(source_dir)

        if len(filenames) == 0:
            log_func("В выбранной папке отсутствуют файлы")
            return None
        if len(filenames) == 1:
            log_func("В выбранной папке недостаточно файлов для сравнения(1)")
            return None

        cur = 0
        last = len(filenames)

        for filename in filenames:
            if ".pdf" in filename:
                try:text = pdfminer.high_level.extract_text("C:/Users/kaspersky/Desktop/cpm/source/test.pdf")
                except Exception as ex:log_func(f"Произошла ошибка во время чтения файла:\n{filename} \nerror:{str(ex)}",True)
            elif ".docx" in filename:
                try:text = " ".join([para.text for para in Document(Path(source_dir, filename)).paragraphs])
                except Exception as ex:log_func(f"Произошла ошибка во время чтения файла:\n{filename} \nerror:{str(ex)}",True)
            elif ".xls" in filename:
                try:text = str(read_excel(Path(source_dir, filename),sheet_name=None).values())
                except Exception as ex:log_func(f"Произошла ошибка во время чтения файла:\n{filename} \nerror:{str(ex)}",True)
            else:
                continue
            creation = datetime.fromtimestamp(os.path.getctime(Path(source_dir, filename))).strftime('%d-%m-%Y %H:%M:%S') 
            update = datetime.fromtimestamp(os.path.getmtime(Path(source_dir, filename))).strftime('%d-%m-%Y %H:%M:%S')
            texts.update({filename:{"text":text,"coef":-1,"pair":{},"creation":creation,"update":update}})
            log_func(f"Сканирование файлов - прогресс {round(100*cur/last,1)}%" )
            cur+=1
                
        log_func(f"Сканирование файлов - прогресс {round(100*cur/last,1)}%" )
        
        if len(texts) == 0:
            log_func("В выбранной папке отсутствуют файлы расширения .xls или xlsx")
            return None

        cur = 0
        last = (len(texts)-1)*len(texts)/2

        texts_t = list(texts.keys())
        for name1 in texts:
            texts_t.remove(name1)
            for name2 in texts_t:
                coef = comparator.compare(texts[name1]["text"],texts[name2]["text"],10)
                if coef > texts[name1]["coef"]:
                    texts[name1]["coef"] = coef
                    texts[name1]["pair"] = name2 
                if coef > texts[name2]["coef"]: 
                    texts[name2]["coef"] = coef
                    texts[name2]["pair"] = name1

                log_func(f"Сравнение файлов - прогресс {round(100*cur/last,1)}%" )
                cur+=1
                
        log_func("Сравнение прошло успешно")
        temp_data.texts = [
            {
                "creation":texts[text]["creation"],
                "update":texts[text]["update"],
                "name":text,
                "pair":texts[text]["pair"],
                "coef":round(texts[text]["coef"],2)
                } for text in texts]
    except Exception as ex:
        log_func(f"Произошла ошибка во время конвертирования:\nerror:{str(ex)}",True)

    
