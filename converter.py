from pandas import read_excel
import os
from pathlib import Path
import comparator
from datetime import datetime,timedelta

class Conv():

    def CMP(self,source_dir:str,log_func = None) -> str:
        ##"""to do закэтчить ошибку неудаётся нати указаный путь когда просто закрываешь окошко"""
            texts = { filename:
                            {
                                "text":str(read_excel(Path(source_dir, filename),sheet_name=None).values()),
                                "coef":-1,
                                "pair":{}
                        } 
                for filename in os.listdir(source_dir)
            }

            cur = 0
            last = (len(texts)-1)*len(texts)/2
            start = datetime.now()
            remain = ""
            passed = ""
            avg = timedelta(0)

            texts_t = list(texts.keys())
            for name1 in texts:
                texts_t.remove(name1)
                for name2 in texts_t:
                    now = datetime.now()
                    coef = comparator.compare(texts[name1]["text"],texts[name2]["text"],10)
                    if coef > texts[name1]["coef"]:
                        texts[name1]["coef"] = coef
                        texts[name1]["pair"] = name2 
                    if coef > texts[name2]["coef"]: 
                        texts[name2]["coef"] = coef
                        texts[name2]["pair"] = name1

                    if log_func != None:
                        delta = datetime.now() - now
                        avg = (avg*cur+delta)/(cur+1) if avg != timedelta(0) else delta
                        remain:timedelta = (avg*(last-cur))
                        passed:timedelta = datetime.now() - start
                        log_str = f"Прогресс {round(100*cur/last,1)}% \n" + \
                                f"Осталось: {int(remain.seconds/3600)} час {int(remain.seconds/60)%60} мин {remain.seconds%60} сек   \n" + \
                                f"Прошло: {int(passed.seconds/3600)} час {int(passed.seconds/60)%60} мин {passed.seconds%60} сек   \n"
                        log_func(log_str)
                        cur+=1

            if log_func != None:
                log_str = f"Прогресс {round(100*cur/last,1)}% " + \
                                f"Осталось: {int(remain.seconds/3600)} час {int(remain.seconds/60)%60} мин {remain.seconds%60} сек \n" + \
                                f"Прошло: {int(passed.seconds/3600)} час {int(passed.seconds/60)%60} мин {passed.seconds%60} сек   \n"
                log_func(log_str)

        
            return [{"name":it,"coef":texts[it]["coef"],"pair":texts[it]["pair"]} for it in texts]
        


 










