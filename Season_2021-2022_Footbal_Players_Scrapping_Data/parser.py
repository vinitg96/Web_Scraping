import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re


def get_table(url):

    """Retorna DataFrame com estatísticas dos jogadores apartir de uma URL"""
    
    site = requests.get(url)
    bs = BeautifulSoup(site.content, "html.parser")
    
    players_table = bs.find("table", {"id":re.compile("stats_standard")})
    
    league = bs.find("div", {"id": "meta"}).find("span", {"class":"header_end"}).get_text().replace(")", "").replace("(", "")
    club_name = players_table.find("span").get_text()
    club_name = club_name[club_name.find(" "):club_name.find(":")].strip()
    
    headers_table = []
    for column_name in players_table.thead.find_all("tr")[1]: #thead é onde estão os cabeçalhos da tabela
        header_table = column_name.get_text()
        if header_table == " ": 
            continue
        headers_table.append(header_table)
    
    df = pd.DataFrame(columns=headers_table)

    for row in players_table.tbody.find_all("tr"): #iterar por todas as linhas, o nome não está em //td
        player_name = row.find("th").get_text()
        row_data = [i.get_text() for i in row.find_all("td")]
        row_data.insert(0,player_name)
        df.loc[len(df)] = row_data #df inicia com len = 0 e aumenta a cada iteração
    
    df["Liga"] = league
    df["Clube"] = club_name

    return df


def format_table(df):

    """Retorna um DataFrame formatado"""
    
    df = df.replace("", np.nan)
    df = df.dropna()

    #ajuste das "," e "."
    for i in range(len(df.columns)):
        df.iloc[:,i] = df.iloc[:,i].apply(lambda x: str(x).replace(",","."))

    df["Min."] = df["Min."].apply(lambda x: str(x).replace(".",""))
    
    #formatar sigla do país
    df["Nação"] = df["Nação"].apply(lambda x: x[str(x).find(" "):].strip())
    
    #remover colunas desnecessárias
    df.iloc[:, 15:30] = np.nan
    df = df.dropna(axis=1)
    
    #formatar coluna de posição
    l1 = ["ZG", "LE", "LD", "CB"]
    d1 = dict.fromkeys(l1, 'DEF')

    l2 = ["LT", "MC", "ME", "MD", "GM", "MA"]
    d2 = dict.fromkeys(l2, 'MEI')

    l3 = ["AT", "PE", "PD"]
    d3 = dict.fromkeys(l3, 'ATA')

    d4 = {"G":"GK"}

    d5 = dict(d1)
    d5.update(d2)
    d5.update(d3)
    d5.update(d4)
    
    df["Pos."] = df["Pos."].str.split(".", expand=True).rename(columns={0:"Pos1",1:"Pos2"}).iloc[:,0].map(d5)

    #ordernar colunas
    cols_order = ['Jogador', 'Liga','Clube', 'Nação', 'Pos.', 'Idade', 'MP', 'Inícios', 'Min.', '90s', 'Gols', 'Assis.', 'G-PB', 'PB', 'PT', 'CrtsA', 'CrtV']
    df = df[cols_order]        

    #ajustar tipos de variáveis
    int_cols = ["Idade","MP","Inícios","Min.", "Gols","Assis.","G-PB", "PB", "PT","CrtsA","CrtV"]
    float_cols = ["90s"]
    
    for col in int_cols:
        df[col] = df[col].astype(int)
        
    for col in float_cols:
        df[col] = df[col].astype(float)
    
    #criar novas features
    df["G_90"] = (df["Gols"] / df["90s"]).round(2)
    df["A_90"] = (df["Assis."] / df["90s"]).round(2)
    df["G+A_90"] = ((df["Gols"] + df["Assis."]) / df["90s"]).round(2)
    
    #garantir que nao tenha NA
    df = df.dropna()
    
    return df
