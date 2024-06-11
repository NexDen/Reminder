import csv, os
from tkinter import*
from datetime import*
from datetime import timedelta

width = 300
height = 170
font = "Segoe UI Light"
hatırlatıcı_path = "C:/Users/yigit/Desktop/HATIRLATICI/hatırlatıcılar.csv"

pencereler = []
hatırlatıcılar = []

rows = [
    "İsim",
    "Yıl",
    "Ay",
    "Gün",
    "Saat",
    "Dakika",
    "Saniye",
    "xSaniyeKaldığıZamanGöster",
    "İkonLink",
]


def hatırlatıcı_bitti(biten_hatırlatıcı):
    global hatırlatıcılar

    with open(hatırlatıcı_path, mode='w', encoding="utf-8") as csv_file:
        csv_file.truncate(0)
        csv_writer = csv.DictWriter(csv_file, restval="0", fieldnames=rows)
        to_write = {}
        for row_name in rows:
            to_write[row_name] = row_name
        csv_writer.writerow(
            to_write
        ) 
        to_write = {}
        for hatırlatıcı in hatırlatıcılar: # tamamlanan hatırlatıcı dışında hepsini listeye geri yaz
            if biten_hatırlatıcı != hatırlatıcı: 
                for row_name in rows:
                    to_write[row_name] = hatırlatıcı[row_name]
                csv_writer.writerow(
                    to_write
                )
                

def pencere_güncelle(): #hold up
    global pencereler, hatırlatıcılar
    global selin # globel selyn
    for pencere in pencereler:
        pencere.destroy()
    pencereler = []
    hatırlatıcılar = []
    with open(hatırlatıcı_path, mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, restval="0", fieldnames=rows)
        for index, row in enumerate(csv_reader, start=-1):
            if index == -1:
                continue
            # print(row)
            pencere = Tk()
            pencere.config(bg="black")
            pencere.geometry(f"{width}x{height}+{pencere.winfo_screenwidth()-width}+{10+(index*height)}")
            
            pencere.overrideredirect(True)
            pencere.attributes("-transparentcolor","black")

            label_başlık = Label(pencere, name=f"{index}-başlık", font=(font, 20), bg="black", fg="white")
            label_başlık.pack()

            label_gün = Label(pencere, name=f"{index}-gün", font=(font, 48), bg="black", fg="white")
            label_gün.pack()

            label_diğer = Label(pencere, name=f"{index}-diğer", font=(font, 10), bg="black", fg="white")
            label_diğer.pack()

            pencereler.append(pencere)
            hatırlatıcılar.append(row)

            # print(row)

def timedelta_to_dhms(string):
    string = string.split(":")
    # print(string)
    if "days" in string[0] or "day" in string[0]:
        day = int(string[0].split(",")[0].removesuffix("days").removesuffix("day")) # evet removesuffix fuck you
        hour = int(string[0].split(",")[1])
    else:
        day = 0
        hour = int(string[0])
    minute = int(float(string[1]))
    second = int(float(string[2]))

    day = 0 if day < 0 else day
    hour = 0 if hour < 0 else hour
    minute = 0 if minute < 0 else minute
    second = 0 if second < 0 else second  

    # print(day, hour, minute, second)
    return (day, hour, minute, second)

def main():
    global başlık_widget, gün_widget, diğer_widget
    pencere_güncelle()
    # print(pencereler)

    last_modified_last = os.stat(hatırlatıcı_path).st_mtime # program ilk açıldığındaki default değişim zamanı
    while True: # her 10 ms de bir
        last_modified = os.stat(hatırlatıcı_path).st_mtime
        if last_modified_last != last_modified: # eğer hatırlatıcılar dosyası değişti ise (son değiştirildi tarihi değişti ise) tekrardan update_windows() çağır
            pencere_güncelle()
            last_modified_last = last_modified
        pencere_index = 0
        for index, pencere in enumerate(pencereler):
            if index > 6: #6. pencereden sonrasıyla uğraşma bile (opt.)
                continue
            pencere.geometry(f"{width}x{height}+{pencere.winfo_screenwidth()-width}+{10+(pencere_index*height)}") # ekran değişikliklerinde bozulmasın diye
            başlık = hatırlatıcılar[index]["İsim"] # YKS
            başlık_widget = pencere.nametowidget(f"{index}-başlık")

            gün_widget = pencere.nametowidget(f"{index}-gün")
            diğer_widget = pencere.nametowidget(f"{index}-diğer")
            try:
                hedef = datetime(
                    int(hatırlatıcılar[index]["Yıl"]),
                    int(hatırlatıcılar[index]["Ay"]),
                    int(hatırlatıcılar[index]["Gün"]),
                    int(hatırlatıcılar[index]["Saat"]),
                    int(hatırlatıcılar[index]["Dakika"]),
                    int(hatırlatıcılar[index]["Saniye"]),
                )
            except Exception: # eğer herhangi bir değer yanlış girildiyse/eksik girildiyse HATALI GİRİŞ ver ve programı kapattırma
                başlık_widget.config(fg="red", text="HATALI GİRİŞ")
                gün_widget.config(fg="red", text="HATALI GİRİŞ", font=(font, 35))
                diğer_widget.config(fg="red", text="HATALI GİRİŞ")
                continue
            try:
                if hatırlatıcılar[index]["İkonLink"] != "0":
                    open(hatırlatıcılar[index]["İkonLink"].strip())
            except Exception:
                başlık_widget.config(fg="red", text="HATALI İKON")
                gün_widget.config(fg="red", text="HATALI İKON", font=(font, 35))
                diğer_widget.config(fg="red", text="HATALI İKON")
            şuan = datetime.now()
            sec = (hedef-şuan).total_seconds()
            td_str = str(timedelta(seconds=sec))
            gün, saat, dakika, saniye = timedelta_to_dhms(td_str)
            saniye = int(float(saniye))
            if sec > 0:
                if sec < int(hatırlatıcılar[index]["xSaniyeKaldığıZamanGöster"]) or not int(hatırlatıcılar[index]["xSaniyeKaldığıZamanGöster"]):
                    başlık_widget.config(text=başlık)
                    if gün == 0:
                        if hedef.day != şuan.day:
                            gün_str = "YARIN"
                            diğer_widget.config(text=f"{f'{saat} SAAT' if int(saat) else ''}{f' {dakika} DAKİKA' if int(dakika) else ''}{f' {saniye} SANİYE' if saniye else ''}")
                        else:
                            if saat:
                                gün_widget.config(font=(font, 20))
                                gün_str = f"{saat} SAAT\n{dakika} DAKİKA\n{saniye} SANİYE"
                            elif dakika:
                                gün_widget.config(font=(font, 30))
                                gün_str = f"{dakika} DAKİKA\n{saniye} SANİYE"
                            else:
                                gün_widget.config(font=(font, 40))
                                gün_str = f"{saniye} SANİYE"

                    else:
                        gün_str = f"{gün} GÜN"
                        diğer_widget.config(text=f"{f'{saat} SAAT' if int(saat) else ''}{f' {dakika} DAKİKA' if int(dakika) else ''}{f' {saniye} SANİYE' if saniye else ''}")
                    gün_widget.config(text=gün_str)
                else:
                    continue
            else:
                hatırlatıcı_bitti(hatırlatıcılar[index]) # eğer saniye < 0 ise hatırlatıcıyı tamamla ve listeden sil
            pencere.after(10) # 10ms bekle ve tekrardan güncelle (ki donmasın)
            pencere.update()
            pencere_index+=1

try:
    main()
except Exception as e:
    print(e)
    şuan = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    with open(rf"C:\Users\thene\Desktop\HATIRLATICI\hatırlatıcı_hata_{şuan}.txt", "w", encoding="utf-8") as f:
        f.write(f"{type(e)} {str(e)}")
