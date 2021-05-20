import pandas as pd
import codecs

translate_dict = pd.read_csv("dict.csv")

with codecs.open('areas.yaml', 'r', encoding="UTF-8") as f_i:
    data = str(f_i.read())
    #print(data)

    for i in range(0,len(translate_dict)):
        jp = translate_dict.iat[i, 0]
        en = translate_dict.iat[i, 3]
        #print(jp,en)
        data = data.replace(jp, en)

with codecs.open('areas_en.yaml', 'w', encoding="UTF-8") as f_o:
    f_o.write(data)
