from crawler import crawler
from parser import get_table, format_table
import time
import pandas as pd
import json
import os

clear = lambda: os.system('clear')


URL = "https://fbref.com/pt/comps/Big5/Maiores-5-Ligas-Europeias-Estatisticas"
table_id = "big5_table"


def main():
    start_time = time.time()

    urls_dic = crawler(URL, table_id)

    a_file = open("urls_dic.json", "w")
    json.dump(urls_dic, a_file)
    a_file.close()

    
    print("\n\nObtendo tabelas e formatando DataFrame final")

    list_of_dfs = []
    i = 1
    for name, url in urls_dic.items():
        time.sleep(10) #tempo para não sobrecarregar o servidor
        df = get_table(url)
        df = format_table(df)
        
        list_of_dfs.append(df)
        print(f"{name} --------- OK------------- {i} \ {len(urls_dic)} ")
        
        i+=1

    final_df = pd.concat(list_of_dfs, ignore_index=True)
    final_df.to_csv("df_data_players.csv", index=False)
    clear()
    print(f"Tempo de execução: {round(time.time() - start_time, 2)} segundos")

if __name__ == "__main__" :
    main()