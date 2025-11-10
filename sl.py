
#Detta skript skapar en Tray ikon Program för att se avgångar för SL-trafiken i realtid.

import os
import requests
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import *
import pystray
from pystray import MenuItem as item
from PIL import Image

#Lägg in din avgång här: t.ex site_id = 9001 (T-centralen)
site_id = 1327

# Skapa API-funktion
def sl_api():
    #Hämta API
    response = requests.get(
        f"https://transport.integration.sl.se/v1/sites/{site_id}/departures")
    
    #Öppna upp API
    sl_data = response.json()
    
    #Skapa tabell
    df = pd.DataFrame(sl_data["departures"])
    
    #Packa upp nästlade kolumner
    df = pd.json_normalize(sl_data["departures"])
    
    #Välj dem kolumner som är intressanta att visa
    df = df[["stop_area.name", "line.id", "destination", "display", 
             "expected", "line.transport_mode"]]
    
    #Byt namn på kolumner
    df = df.rename(columns={
        "stop_area.name": "Hållplats/ Station",
        "line.id": "Linje",
        "destination": "Mot",
        "display": "Avgår om",
        "expected": "Tid",
        "line.transport_mode": "Färdmedel" })
    
    #Gör om tid till endast HH:MM
    df["Tid"] = pd.to_datetime(df["Tid"]).dt.strftime("%H:%M")
    
    #Ändra tunnelbanenummer
    df["Linje"] = df["Linje"].astype(str).replace(linjer)
    #Ändra namn på färdmedel
    df["Färdmedel"] = df["Färdmedel"].astype(str).replace(färdmedel)

    return df
# ---------------------------------------
#Ändra namn

linjer = {
    "10": "Blåa",
    "11": "Blåa",
    "13": "Röda",
    "14": "Röda",
    "17": "Gröna",
    "18": "Gröna",
    "19": "Gröna",
    "7": "Spårväg City",
    "12": "Nockebybanan",
    "21": "Lidingöbanan",
    "25": "Saltsjöbanan",
    "26": "Saltsjöbanan",
    "27": "Roslagsbanan",
    "28": "Roslagsbanan",
    "29": "Roslagsbanan",
    "30": "Tvärbanan",
    "31": "Tvärbanan"
}

färdmedel = {
    "BUS": "Buss", 
    "METRO": "Tunnelbana",
    "SHIP": "Båt",
    "TRAM": "Övrig spårtrafik",
    "TRAIN": "Pendeltåg"
}

#----------------------------------------

#Skapa GUI Fönster
window = tk.Tk()
window_width = 400
window_height = 300

#Placera nere i högra hörnet
window.geometry(f'{window_width}x{window_height}+{1130}+{495}')
window.resizable(False, False)

#lås fönster
def lock_window(event):
    window.geometry(f'{window_width}x{window_height}+{1130}+{495}')

window.bind("<Configure>", lock_window)

window.title('SL-avgångar')
window.withdraw() #Göm fönstret vid start

# Göm fönstret vid tryck på X i GUI
def hide_window():
    window.withdraw()
window.protocol("WM_DELETE_WINDOW", hide_window)

#----------------------------------------
#Skapa Hållplats-Dropdown

#Skapa dictionary med hållplatser + IDn
stationer = {
    "Nytorgsgatan": 1327,
    "Frihamnsporten": 1171,
    "Slussen": 9192,
    "Gärdet": 9221,
    "Hötorget": 9119,
    "Karolinska institutet västra": 3404,
    "Ropsten": 9220
}

# Ändra hållplats-ID, site_id
def byt_hållplats(event):
    global site_id
    vald_hållplats = dropdown_menu.get()
    site_id = stationer[vald_hållplats]
    update_table()

# variabel som endast visar hållplats från stationer, inte ID
hållplatser = list(stationer.keys())

#Combo box - För Hållplatser
l1=Label(window, text="Hållplats/ Station")
l1.grid(row = 0, column= 0)
dropdown_menu = ttk.Combobox(window, value=hållplatser, width=15)
dropdown_menu.current(0)
dropdown_menu.grid(row = 1, column= 0, padx=10, pady=(0,40))
dropdown_menu.bind("<<ComboboxSelected>>", byt_hållplats)

#----------------------------------------
#Skapa Dropdown för Färdmedel

#Skapa ett standardval
valt_färdmedel = "Buss"

alternativ_färdmedel = ["Buss", "Tunnelbana", "Båt", "Övrig spårtrafik", "Pendeltåg"]

# Funktion = Ändra Färdmedel
def byt_färdmedel(event):
    global valt_färdmedel
    valt_färdmedel = dropdown_menu_2.get()
    update_table()

#Skapa Combobox för Färdmedel
l2=Label(window, text="Färdmedel")
l2.grid(row = 0, column= 5)
dropdown_menu_2 = ttk.Combobox(window, value=alternativ_färdmedel, width=15)
dropdown_menu_2.current(0)
dropdown_menu_2.grid(row = 1, column= 5, padx=10, pady=(0,40))
dropdown_menu_2.bind("<<ComboboxSelected>>", byt_färdmedel)

#----------------------------------------
# treeview - Skapa tabell
sl_tabell = ttk.Treeview(window, columns = (
    'Hållplats', 'Linje', 'Mot', 'Avgår om', 'Tid'), show = 'headings')

#Skapa column-rubriker
sl_tabell.heading('Hållplats', text= 'Hållplats/ Station')
sl_tabell.heading('Linje', text= 'Linje')
sl_tabell.heading('Mot', text= 'Mot')
sl_tabell.heading('Avgår om', text= 'Avgår om')
sl_tabell.heading('Tid', text= 'Tid')
#sl_tabell.heading('Färdmedel', text= 'Färdmedel')

# Ändra kolumnbredd
sl_tabell.column('Hållplats', width=120)
sl_tabell.column('Linje', width=45)
sl_tabell.column('Mot', width=120)
sl_tabell.column('Avgår om', width=70)
sl_tabell.column('Tid', width=45)
#sl_tabell.column('Färdmedel', width=70)

sl_tabell.grid(row=4, column=0, columnspan=6)

#----------------------------------------
# Hämta data & lägg in i tabellen och uppdatera
def update_table():
    #Hämta DataFrame
    df = sl_api()
    
    #Filtrera på färdmedel
    df = df[df["Färdmedel"] == valt_färdmedel]

    #Töm tabell
    sl_tabell.delete(*sl_tabell.get_children())

    #Max antal rader åt gången
    max_rows = 9

    #Lägg in data i GUI tabell
    for index, row in df.head(max_rows).iterrows():
        sl_tabell.insert('', 'end', values=(row["Hållplats/ Station"], 
                                            row["Linje"], 
                                            row["Mot"], 
                                            row["Avgår om"], 
                                            row["Tid"], 
                                            row["Färdmedel"]))
    #Uppdatera efter 15 sekunder 
    window.after(15000, update_table)

update_table()

#----------------------------------------
#Skapa Tray-ikon

#funktion som triggas när man trycker på ikon.
def on_clicked(icon, item):
    if str(item) == "Visa avgångar":
        window.deiconify()
    elif str(item) == "Avsluta":
        window.quit() #Stäng Tkinter
        icon.stop() #stänger ner ikon

#Image   
def icon_menu():
    #lägg in sökväg för image
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "sl_icon.png")
    
    image = Image.open(icon_path)
    menu = pystray.Menu(
        pystray.MenuItem("Visa avgångar", on_clicked),
        pystray.MenuItem("Avsluta", on_clicked)
    )
    sl_tray_icon = pystray.Icon("SL", image, "SL", menu)
    #starta ikon i bakgrunden 
    sl_tray_icon.run_detached()

icon_menu()
window.mainloop()

#----------------------------------------
