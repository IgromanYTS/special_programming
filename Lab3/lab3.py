#Імопортуємо модулі
from spyre import server
import pandas as pd
import urllib
import json
import os
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

#Повторюємо операцію формування Датафрейму з лаб2
directory_name = "Lab3/node"

dicti = {
    1 : 24,
    2 : 25,
    3 : 5,
    4 : 6,
    5 : 27,
    6 : 23,
    7 : 26,
    8 : 7,
    9 : 11,
    10 : 13,
    11 : 14,
    12 : 15,
    13 : 16,
    14 : 17,
    15 : 18,
    16 : 19,
    17 : 21,
    18 : 22,
    19 : 8,
    20 : 9,
    21 : 10,
    22 : 1,
    23 : 3,
    24 : 2,
    25 : 4,
    26 : 12,
    27 : 20
    }

headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
data = pd.DataFrame(columns=headers)
for i in range(1,29):
    name = f"NOAA_ID{i}_*.csv"
    file_list = glob.glob(os.path.join(directory_name, name))
    for file_path2 in file_list:
        df = pd.read_csv(file_path2, header = 1, names = headers)
        df = df.drop(df.loc[df['VHI'] == -1].index)
        df['area'] = i
        df = df[~df['Year'].astype(str).str.contains('<|>', regex=True)]
        #df = df.dropna()
        data = pd.concat([data, df], ignore_index=True)
data = data.drop(data.columns[[-2]], axis=1)

for i in range(1,28):
    data.loc[data["area"]==dicti[i], "area"] = i
print(data)

#Клас для модуля spyre
class StockExample(server.App):
    #Назва
    title = "NOAA DATA VISUALIZATION"
    #Робимо всі необхадні способи прийому інформації
    inputs = [{        "type":'dropdown',
                    "label": 'NOAA data dropdown',
                    "options" : [ {"label": "VCI", "value":"VCI"},
                                  {"label": "TCI", "value":"TCI"},
                                  {"label": "VHI", "value":"VHI"}],
                    "key": 'option',
                    "action_id": "update_data"},

                    {        "type":'dropdown',
                    "label": 'NOAA data dropdown',
                    "options" : [ {"label": "1:Vinnytsya", "value":"1"},
                                  {"label": "2.Volyn", "value":"2"},
                                  {"label": "3.Dnipro", "value":"3"},
                                  {"label": "4.Donetsk", "value":"4"},
                                  {"label": "5.Zhytomyr", "value":"5"},
                                  {"label": "6.Transcarpathia", "value":"6"},
                                  {"label": "7.Zaporizhzhya", "value":"7"},
                                  {"label": "8.Ivano-Frankivs'k", "value":"8"},
                                  {"label": "9.Kiev", "value":"9"},
                                  {"label": "10.Kirovohrad", "value":"10"},
                                  {"label": "11.Luhans'k", "value":"11"},
                                  {"label": "12.L'viv", "value":"12"},
                                  {"label": "13.Mykolayiv", "value":"13"},
                                  {"label": "14.Odessa", "value":"14"},
                                  {"label": "15.Poltava", "value":"15"},
                                  {"label": "16.Rivne", "value":"16"},
                                  {"label": "17.Sumy", "value":"17"},
                                  {"label": "18.Ternopil'", "value":"18"},
                                  {"label": "19.Kharkiv", "value":"19"},
                                  {"label": "20.Kherson", "value":"20"},
                                  {"label": "21.Khmel'nyts'kyy", "value":"21"},
                                  {"label": "22.Cherkasy", "value":"22"},
                                  {"label": "23.Chernivtsi", "value":"23"},
                                  {"label": "24.Chernihiv", "value":"24"},
                                  {"label": "25.Crimea", "value":"25"},
                                  {"label": "26.Kiev City", "value":"26"},
                                  {"label": "27.Sevastopol'", "value":"27"},
                                  ],
                    "key": 'city',
                    "action_id": "update_data"},

                
                   {
    "type":'slider',
    "label": 'Indicate the year of the beginning of the interval:',
    "key": 'begin',
    "value" : 2000,
    "min" : 1982,
    "max" : 2024,
    "action_id" : "update_data",
    "linked_key": 'title',
    "linked_type": 'text',
}, 
{
    "type":'slider',
    "label": 'Indicate the year of the end of the interval:',
    "key": 'end',
    "value" : 2010,
    "min" : 1982,
    "max" : 2024,
    "action_id" : "update_data",
    "linked_key": 'title',
    "linked_type": 'text',
}, dict( type="text",
                   key="range",
                   label="specify to weekly interval",
                   value="1,2",
                   action_id="simple_html_output")

                    ]
    
    #inputs = []

    controls = [{    "type" : "hidden",
                    "id" : "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
                { "type" : "table",
                    "id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True }]
    #Функція формування таблиці
    def getData(self, params):
        # Приймаємо змінні
        indicator = str(params['option'])  
        region = int(params['city']) 
        start_year = str((params['begin'])-1)  
        end_year = str((params['end']))  
        week = (params['range'].split(','))
        week_start = float((week[0].strip()) ) 
        week_end = float((week[1].strip()))

        #print(indicator, region, start_year, end_year)
        #print(weeks_range)

        #print(week_start, week_end)

        # Фільтруємо данні за змінними
        filtered_data = data[(data['area'] == region) &
                         (data['Year'] >= start_year) &
                         (data['Year'] <= end_year) &
                          (data['Week'] >= week_start) & (data['Week'] <= week_end)
                ]
        # Повертаємо
        return filtered_data[['Year', 'Week', indicator]]

    # Формуємо графік
    def getPlot(self, params):
        #Використовуємо дані таблиці
        df_f = self.getData(params).set_index(['Year', 'Week'])

        
        obj = df_f.plot(figsize=(15, 6))

        fig = obj.get_figure()
        return fig


    def getHTML(self, params):
        range = params["range"]
        return range

app = StockExample()
app.launch(port=9093)