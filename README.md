# SL-departures
## Real­tids­avgångar från SL med systemtray och GUI

<img width="557" height="500" alt="2" src="https://github.com/user-attachments/assets/0728be9b-9d91-4995-96ec-32fe3dfd61ee" />


## Gui
Visar realtidsavgångar från SL direkt i ett litet GUI-fönster och system tray.  
Du kan välja både **hållplats** och **färdmedel** (Buss, Tunnelbana, Båt, Pendeltåg och Övrig spårtrafik såsom Tvärbanan, Spårväg city mm), och avgångarna uppdateras automatiskt.

## Funktioner
- System tray-icon (programmet kan köras i bakgrunden)
- Dropdown för att välja hållplats
- Dropdown för att välja färdmedel
- Visar kommande avgångar i realtid
- Uppdateras automatiskt var 15:e sekund
- Låst fönsterposition (kan inte flyttas av misstag)

## Skräddarsy din egen app
1. Kör skriptet **SL_hållplatsID.py** för att söka efter hållplatsnamn och få fram dess **site_id**.
2. Kopiera de site_id du vill använda.
3. Öppna huvudprogrammet **sl.py** och ersätt värdet på `site_id` på **rad 14** och på **rad 100**
<img width="928" height="499" alt="image" src="https://github.com/user-attachments/assets/bccddd83-c472-4812-8e5a-affb242c0f1f" />
<img width="716" height="347" alt="image" src="https://github.com/user-attachments/assets/0ca2772a-de62-4ed1-98c0-f048a0bc07a3" />





