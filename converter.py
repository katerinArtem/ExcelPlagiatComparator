from pandas import read_excel
import os
from pathlib import Path
import comparator
from datetime import datetime
import temp_data

def CMP(source_dir:str,log_func):
    ##"""to do закэтчить ошибку неудаётся нати указаный путь когда просто закрываешь окошко"""
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
            if ".xls" not in filename and ".xlsx" not in filename:continue 
            text = str(read_excel(Path(source_dir, filename),sheet_name=None).values())
            creation = datetime.fromtimestamp(os.path.getctime(Path(source_dir, filename))).strftime('%d-%m-%Y %H:%M:%S') 
            update = datetime.fromtimestamp(os.path.getmtime(Path(source_dir, filename))).strftime('%d-%m-%Y %H:%M:%S') 
            coef = -1
            pair = {}
            texts.update({filename:{"text":text,"coef":coef,"pair":pair,"creation":creation,"update":update}})

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

    
