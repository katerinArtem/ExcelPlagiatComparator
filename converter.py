from pandas import read_excel
import os
from pathlib import Path
import comparator
from datetime import datetime,timedelta
import threading
import asyncio
import temp_data

def CMP(source_dir:str,log_func = None):
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
            coef = -1
            pair = {}
            texts.update({filename:{"text":text,"coef":coef,"pair":pair}})

            if log_func != None:
                    log_str = f"Сканирование файлов - прогресс {round(100*cur/last,1)}%" 
                    log_func(log_str)
                    cur+=1

        if log_func != None:
            log_str = f"Сканирование файлов - прогресс {round(100*cur/last,1)}%" 
            log_func(log_str)
        

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

                if log_func != None:
                    log_str = f"Сравнение файлов - прогресс {round(100*cur/last,1)}%" 
                    log_func(log_str)
                    cur+=1

        if log_func != None:
            log_str = f"Сравнение файлов - прогресс {round(100*cur/last,1)}%" 
            log_func(log_str)
            
        log_func("Сравнение прошло успешно")
        
        temp_data.texts = [{"name":it,"coef":texts[it]["coef"],"pair":texts[it]["pair"]} for it in texts]

    
        


 










