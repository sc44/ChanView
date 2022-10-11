#! /usr/bin/env python3
#
#  ChanView v1.00 - Update: 10.10.2022
#
#  getestet mit:  LG-TV UM7100PLA - webOS 4.9.5-14
#
###############################################################################################################

import tkinter as tk
import tkinter.messagebox as message
import tkinter.filedialog as fdialog
import os
import time

###############################################################################################################

# Channel-List
prNum, minorNum, original_network_id, transport_id, service_id, serviceType, frequency, mapAttr = [], [], [], [], [], [], [], []
favoriteIdxA, favoriteIdxB, favoriteIdxC, favoriteIdxD, favoriteIdxE, favoriteIdxF, favoriteIdxG, favoriteIdxH = [], [], [], [], [], [], [], []
isInvisable, isBlocked, isSkipped, isDeleted, isScrambled, vchName, isUserSelCHNo, videoStreamType = [], [], [], [], [], [], [],[]

# Service-Info
aucSvcName, usServiceID, bVisibilityFlag, bIsScramble, usLCNValue, ucServiceType, usTPIndex = [],[],[],[],[],[],[]

# Tuning-Info
unFrequency, unTSID, unONID, abwSymbolRate, abwPolarization, abwCodeRate, bwDVBS2 = [],[],[],[],[],[],[] 
abwModulationType, bwDirection, abwAnglePrec, ucAngle, ucNoOfServices, usTPHandle = [],[],[],[],[],[] 

# Satelliten-Info
SatelliteNameHex, Angle, AnglePrec, DirEastWest = [],[],[],[]

# Transponder-Info
TransponderId, Frequency, Polarisation, SymbolRate, TransmissionSystem, HomeTp = [],[],[],[],[],[]

# Transponder-Parameter
uwServiceStartIndex, uwServiceEndIndex, uwServiceCount, nitVersion = [],[],[],[]
channelIndex, frequency2, original_network_id2, transport_id2 = [],[],[],[]

Puffer = []           # alle Dateizeilen
idxDTV = 0            # Pufferindex von <CHANNEL> <DTV>
Index = []            # Index der unsortierten Channel-Elemente

SortListe = []        # Sortierte Elemente
servTypText = []      # serviceType in Klartext

TLLDatei = ""
Editiert = False

Vordergrund = "#ffffcc"
Hintergrund = "#000066"

###############################################################################################################

Master = tk.Tk()
Master.title("Channel View v1.00")
Master.option_add("*Dialog.msg.font", "Helvetica 11")        # Messagebox Schriftart
Master.option_add("*Dialog.msg.wrapLength", "50i")           # Messagebox Zeilenumbruch

Titeltext = tk.StringVar()          # Titelzeile
Statustext = tk.StringVar()         # Statuszeile
Lauftext = tk.StringVar()           # Laufschrift

AttributP = tk.IntVar()             # verschlüsselt
AttributV = tk.IntVar()             # versteckt
AttributU = tk.IntVar()             # überspringen
AttributS = tk.IntVar()             # gesperrt
AttributL = tk.IntVar()             # löschen

Master.geometry("+300+0")           # Fensterposition

###############################################################################################################

def Datei_Oeffnen(event=None):

    global Editiert, TLLDatei

    if Editiert:
        if message.askokcancel("Channel View", "\nEs wurden Einträge geändert. Sollen die Änderungen gespeichert werden?\n"):
            Datei_Speichern()
        Editiert = False

    TLLDatei = fdialog.askopenfilename(initialdir=".", filetypes=[("TV-Dateien","*.TLL"),("Alle Dateien","*")])
    if TLLDatei == ():   TLLDatei = ""

    if os.path.isfile(TLLDatei):
        with open(TLLDatei, "r") as Datei:
            Puffer.clear() 
            for Zeile in Datei:
                Puffer.append(Zeile)
            Datei.close()
        Sender_Loeschen()
        Sender_Laden()
        Alle_Anzeigen()

###############################################################################################################

def Datei_Speichern(event=None):

    if not TLLDatei == "":
        zeit = time.strftime("%Y%m%d%H%M%S")
        os.rename(TLLDatei, TLLDatei + "_" + zeit)
        Datei_Schreiben(TLLDatei)

###############################################################################################################

def Datei_Speichern_Unter():

    Dateiname = fdialog.asksaveasfilename(initialfile=os.path.basename(TLLDatei), filetypes=[("TV-Dateien","*.TLL"),("Alle Dateien","*")])

    if Dateiname:
        Datei_Schreiben(Dateiname)

###############################################################################################################

def Datei_Editor():

    def Datei_Speichern(event):

        Datei = fdialog.asksaveasfile(parent=Fenster, mode="w", initialdir=".", filetypes = [("Alle Dateien","*")])
        if Datei:
            Datei.write(Text_Fenster.get("1.0", tk.END + "-1c"))     # ohne letztes LF !!
            Puffer.clear()
            with open(TLLDatei, "r") as Datei:
                for Zeile in Datei:
                    Puffer.append(Zeile)
                Datei.close()
            Listen_Laden()
            Alle_Anzeigen()
            Fenster.destroy()

    if not os.path.isfile(TLLDatei):
        message.showwarning("Channel View", "\n" + TLLDatei + "nicht gefunden")
    else:
        Fenster = tk.Toplevel(Master)
        Fenster.title(TLLDatei)
        Fenster.geometry("+610+95")
        Fenster.wm_attributes("-topmost", True)     # Fenster immer im Vordergrund halten
        Fenster.wait_visibility()
        Fenster.grab_set()                          # nur dieses Fenster aktiv schalten

        Scroll_Vertikal = tk.Scrollbar(Fenster, width=14)
        Scroll_Horizont = tk.Scrollbar(Fenster, width=14, orient="horizontal")
        Text_Fenster = tk.Text(Fenster, width=70, height=42, pady=10, padx=10, yscrollcommand = Scroll_Vertikal.set, xscrollcommand = Scroll_Horizont.set)
        Text_Fenster.config(fg="#000000", bg="#ffff88", font="Consolas 10", wrap="none", undo="TRUE")
        Zeile_Info = tk.Label(Fenster, font="Helvetica 10", text="Datei speichern mit <Strg+S>  -  Abbrechen mit <Esc>")
        Scroll_Vertikal.config(command = Text_Fenster.yview)
        Scroll_Horizont.config(command = Text_Fenster.xview)
        Zeile_Info.pack(side="bottom", fill="x", padx=2, pady=0)
        Scroll_Vertikal.pack(side="right", fill="y", padx=1, pady=1)
        Scroll_Horizont.pack(side="bottom", fill="x", padx=1, pady=1)
        Text_Fenster.pack(fill="both", padx=2, pady=2, expand=True)
        with open(TLLDatei, "r", newline="\r\n") as Datei:     # \r\n = CRLF statt nur LF
            Text_Fenster.insert("1.0", Datei.read())
            Datei.close()

        Text_Fenster.focus_set()
        Text_Fenster.bind("<Control-Key-s>", Datei_Speichern)
        Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))


###############################################################################################################

def servTypText_Laden(typ):

    if   typ == "1":    return "SD-TV"
    elif typ == "2":    return "Radio"
    elif typ == "3":    return "VText"
    elif typ == "7":    return "FM-Radio"
    elif typ == "10":   return "AAC-Radio"
    elif typ == "12":   return "Data/Test"
    elif typ == "17":   return "HD-TV"
    elif typ == "22":   return "SD-TV"
    elif typ == "25":   return "HD-TV"
    elif typ == "31":   return "UHD-TV"
    elif typ == "159":  return "UHD-TV"
    else:               return "unbekannt"

###############################################################################################################

def Sender_Loeschen():

    servTypText.clear()
    prNum.clear()
    minorNum.clear()
    original_network_id.clear()
    transport_id.clear()
    service_id.clear()
    serviceType.clear()
    frequency.clear()
    mapAttr.clear()
    favoriteIdxA.clear()
    favoriteIdxB.clear()
    favoriteIdxC.clear()
    favoriteIdxD.clear()
    favoriteIdxE.clear()
    favoriteIdxF.clear()
    favoriteIdxG.clear()
    favoriteIdxH.clear()
    isInvisable.clear()
    isBlocked.clear()
    isSkipped.clear()
    isDeleted.clear()
    isScrambled.clear()
    vchName.clear()
    isUserSelCHNo.clear()
    videoStreamType.clear()

###############################################################################################################

def Sender_Laden():

    global idxDTV

    for a in range(0, len(Puffer)-1, 1):
        if Puffer[a] == "<CHANNEL>\n":
            for a in range(a, len(Puffer)-1, 1):
                if Puffer[a] == "<DTV>\n":
                    idxDTV = a
                    a += 1           # Zeiger auf ersten Eintrag: <CHANNEL> <DTV> <ITEM>
                    i = 0
                    while Puffer[a+i*42] != "</DTV>\n":
                        i += 1
                        n = Puffer[a+(i*42-41)].find('</', 7)
                        prNum.append(Puffer[a+(i*42-41)][7:n])
                        n = Puffer[a+(i*42-40)].find('</', 10)
                        minorNum.append(Puffer[a+(i*42-40)][10:n])
                        n = Puffer[a+(i*42-39)].find('</', 21)
                        original_network_id.append(Puffer[a+(i*42-39)][21:n])
                        n = Puffer[a+(i*42-38)].find('</', 14)
                        transport_id.append(Puffer[a+(i*42-38)][14:n])
                        n = Puffer[a+(i*42-36)].find('</', 12)
                        service_id.append(Puffer[a+(i*42-36)][12:n])
                        n = Puffer[a+(i*42-33)].find('</', 13)
                        serviceType.append(Puffer[a+(i*42-33)][13:n])
                        n = Puffer[a+(i*42-31)].find('</', 11)
                        frequency.append(Puffer[a+(i*42-31)][11:n])
                        n = Puffer[a+(i*42-28)].find('</', 9)
                        mapAttr.append(Puffer[a+(i*42-28)][9:n])
                        n = Puffer[a+(i*42-26)].find('</', 14)
                        favoriteIdxA.append(Puffer[a+(i*42-26)][14:n])
                        n = Puffer[a+(i*42-25)].find('</', 14)
                        favoriteIdxB.append(Puffer[a+(i*42-25)][14:n])
                        n = Puffer[a+(i*42-24)].find('</', 14)
                        favoriteIdxC.append(Puffer[a+(i*42-24)][14:n])
                        n = Puffer[a+(i*42-23)].find('</', 14)
                        favoriteIdxD.append(Puffer[a+(i*42-23)][14:n])
                        n = Puffer[a+(i*42-22)].find('</', 14)
                        favoriteIdxE.append(Puffer[a+(i*42-22)][14:n])
                        n = Puffer[a+(i*42-21)].find('</', 14)
                        favoriteIdxF.append(Puffer[a+(i*42-21)][14:n])
                        n = Puffer[a+(i*42-20)].find('</', 14)
                        favoriteIdxG.append(Puffer[a+(i*42-20)][14:n])
                        n = Puffer[a+(i*42-19)].find('</', 14)
                        favoriteIdxH.append(Puffer[a+(i*42-19)][14:n])
                        n = Puffer[a+(i*42-18)].find('</', 13)
                        isInvisable.append(Puffer[a+(i*42-18)][13:n])
                        n = Puffer[a+(i*42-17)].find('</', 11)
                        isBlocked.append(Puffer[a+(i*42-17)][11:n])
                        n = Puffer[a+(i*42-16)].find('</', 11)
                        isSkipped.append(Puffer[a+(i*42-16)][11:n])
                        n = Puffer[a+(i*42-14)].find('</', 11)
                        isDeleted.append(Puffer[a+(i*42-14)][11:n])
                        n = Puffer[a+(i*42-11)].find('</', 13)
                        isScrambled.append(Puffer[a+(i*42-11)][13:n])
                        n = Puffer[a+(i*42-8)].find('</', 9)
                        vchName.append(Puffer[a+(i*42-8)][9:n])
                        n = Puffer[a+(i*42-4)].find('</', 15)
                        isUserSelCHNo.append(Puffer[a+(i*42-4)][15:n])
                        n = Puffer[a+(i*42-3)].find('</', 17)
                        videoStreamType.append(Puffer[a+(i*42-3)][17:n])

                        servTypText.append(servTypText_Laden(serviceType[i-1]))      # Klartext: SD, HD, Radio usw.

###############################################################################################################

def Sender_Bearbeiten(event=None):

    def Eintrag_Aendern():

        global Editiert

        if EingabeFav1.get().isnumeric() and EingabeFav2.get().isnumeric() and \
           EingabeFav3.get().isnumeric() and EingabeFav4.get().isnumeric() and EingabeNr.get().isnumeric():

            Editiert = True
            # wenn Sendernummer doppelt dann tauschen
            for i in range(0, len(prNum), 1):
                if prNum[i] == EingabeNr.get() and minorNum[i] != "0":
                    prNum[i] = prNum[Index[cp]]
                    isUserSelCHNo[i] = "1"
                    break
            prNum[Index[cp]] = EingabeNr.get()
            isUserSelCHNo[Index[cp]] = "1"
            vchName[Index[cp]] = EingabeName.get()
            # Favoritenliste schreiben
            favoriteIdxA[Index[cp]] = EingabeFav1.get()
            favoriteIdxB[Index[cp]] = EingabeFav2.get()
            favoriteIdxC[Index[cp]] = EingabeFav3.get()
            favoriteIdxD[Index[cp]] = EingabeFav4.get()
            # Favoriten mapAttribute setzen
            a = 0
            if int(EingabeFav1.get()) < 250:     a += 1
            if int(EingabeFav2.get()) < 250:     a += 2
            if int(EingabeFav3.get()) < 250:     a += 4
            if int(EingabeFav4.get()) < 250:     a += 8
            mapAttr[Index[cp]] = str(a)
            # Channel Attribute setzen
            if AttributP.get():   isScrambled[Index[cp]] = "1"
            else:                 isScrambled[Index[cp]] = "0"
            if AttributV.get():   isInvisable[Index[cp]] = "1"
            else:                 isInvisable[Index[cp]] = "0"
            if AttributU.get():   isSkipped[Index[cp]] = "1"
            else:                 isSkipped[Index[cp]] = "0"
            if AttributS.get():   isBlocked[Index[cp]] = "1"
            else:                 isBlocked[Index[cp]] = "0"
            if AttributL.get():   isDeleted[Index[cp]] = "1"
            else:                 isDeleted[Index[cp]] = "0"
            # evtl. Zeile mit getauschter Nummer neu anzeigen
            for j in range(0, len(Index), 1):
                if prNum[Index[j]] == prNum[i] and minorNum[Index[j]] != "0":
                    Listen_Box.delete(j)
                    Listen_Box.insert(j, "  {:6s} {:5s} {:30.30s} {:10s} {:7s} {:6s} {:6s} {:5s} {:3s} │  {:2s} {:2s} {:2s} {:2s} {:2s} │  {:4s} {:4s} {:4s} {:4s} {:4s} {:4s} {:4s} {:4s}"\
                        .format(prNum[Index[j]], minorNum[Index[j]], vchName[Index[j]], servTypText[Index[j]], frequency[Index[j]],\
                        service_id[Index[j]], transport_id[Index[j]], original_network_id[Index[j]], videoStreamType[Index[j]],\
                        isScrambled[Index[j]], isInvisable[Index[j]], isSkipped[Index[j]], isBlocked[Index[j]], isDeleted[Index[j]],\
                        favoriteIdxA[Index[j]], favoriteIdxB[Index[j]], favoriteIdxC[Index[j]], favoriteIdxD[Index[j]],\
                        favoriteIdxE[Index[j]], favoriteIdxF[Index[j]], favoriteIdxG[Index[j]], favoriteIdxH[Index[j]]))
                    break
            # Zeile mit neuer Nummer neu anzeigen
            Listen_Box.delete(cp)
            Listen_Box.insert(cp, "  {:6s} {:5s} {:30.30s} {:10s} {:7s} {:6s} {:6s} {:5s} {:3s} │  {:2s} {:2s} {:2s} {:2s} {:2s} │  {:4s} {:4s} {:4s} {:4s} {:4s} {:4s} {:4s} {:4s}"\
                .format(prNum[Index[cp]], minorNum[Index[cp]], vchName[Index[cp]], servTypText[Index[cp]], frequency[Index[cp]],\
                service_id[Index[cp]], transport_id[Index[cp]], original_network_id[Index[cp]], videoStreamType[Index[cp]],\
                isScrambled[Index[cp]], isInvisable[Index[cp]], isSkipped[Index[cp]], isBlocked[Index[cp]], isDeleted[Index[cp]],\
                favoriteIdxA[Index[cp]], favoriteIdxB[Index[cp]], favoriteIdxC[Index[cp]], favoriteIdxD[Index[cp]],\
                favoriteIdxE[Index[cp]], favoriteIdxF[Index[cp]], favoriteIdxG[Index[cp]], favoriteIdxH[Index[cp]]))
            Listen_Box.selection_set(cp+1)       # Markierung auf nächste Zeile
            Listen_Box.focus_set()
            Fenster.destroy()

#---------------------------------------------------------------------------

    if len(Index) > 0:
        Fenster = tk.Toplevel(Master)
        Fenster.title("Bearbeiten")
        Fenster.geometry("+640+360")
        Fenster.wm_attributes("-topmost", True)       # Fenster immer im Vordergrund halten
        Fenster.wait_visibility()
        Fenster.grab_set()                            # nur dieses Fenster aktiv schalten

        cp = Listen_Box.curselection()[0]             # Cursor-Position: die markierte Zeile in der Listen_Box
        AttributP.set(int(isScrambled[Index[cp]]))
        AttributV.set(int(isInvisable[Index[cp]]))
        AttributU.set(int(isSkipped[Index[cp]]))
        AttributS.set(int(isBlocked[Index[cp]]))
        AttributL.set(int(isDeleted[Index[cp]]))
        EingabeNr =    tk.Entry(Fenster, bd=3, width=5, font="Helvetica 11")
        EingabeName =  tk.Entry(Fenster, bd=3, width=36, font="Helvetica 11")
        CheckAttrP = tk.Checkbutton(Fenster, bd=3, text=" Pay-TV", font="Helvetica 11", variable=AttributP)
        CheckAttrV = tk.Checkbutton(Fenster, bd=3, text=" Verstecken", font="Helvetica 11", variable=AttributV)
        CheckAttrU = tk.Checkbutton(Fenster, bd=3, text=" Überspringen", font="Helvetica 11", variable=AttributU)
        CheckAttrS = tk.Checkbutton(Fenster, bd=3, text=" Sperren", font="Helvetica 11", variable=AttributS)
        CheckAttrL = tk.Checkbutton(Fenster, bd=3, text=" Löschen", font="Helvetica 11", variable=AttributL)
        TextFav1 = tk.Label(Fenster, text="Fav 1: ", font="Helvetica 11")
        TextFav2 = tk.Label(Fenster, text="Fav 2: ", font="Helvetica 11")
        TextFav3 = tk.Label(Fenster, text="Fav 3: ", font="Helvetica 11")
        TextFav4 = tk.Label(Fenster, text="Fav 4: ", font="Helvetica 11")
        EingabeFav1 =  tk.Entry(Fenster, bd=3, width=4, font="Helvetica 11")
        EingabeFav2 =  tk.Entry(Fenster, bd=3, width=4, font="Helvetica 11")
        EingabeFav3 =  tk.Entry(Fenster, bd=3, width=4, font="Helvetica 11")
        EingabeFav4 =  tk.Entry(Fenster, bd=3, width=4, font="Helvetica 11")
        ButtonSpeichern = tk.Button(Fenster, bd=3, text="Übernehmen", font="Helvetica 11", command=Eintrag_Aendern)
        ButtonAbbrechen = tk.Button(Fenster, bd=3, text="Abbrechen", font="Helvetica 11", command=Fenster.destroy)
        # 1. Zeile mit 10 Spalten
        tk.Label(Fenster).grid(row=0, column=0, padx=30, pady=5)
        tk.Label(Fenster).grid(row=0, column=1, padx=25)
        tk.Label(Fenster).grid(row=0, column=2, padx=30)
        tk.Label(Fenster).grid(row=0, column=3, padx=25)
        tk.Label(Fenster).grid(row=0, column=4, padx=30)
        tk.Label(Fenster).grid(row=0, column=5, padx=25)
        tk.Label(Fenster).grid(row=0, column=6, padx=30)
        tk.Label(Fenster).grid(row=0, column=7, padx=25)
        tk.Label(Fenster).grid(row=0, column=8, padx=30)
        tk.Label(Fenster).grid(row=0, column=9, padx=20)
        # 2. Zeile
        EingabeNr.grid(row=1, column=1, columnspan=1, padx=10, sticky="w", pady=10)
        EingabeName.grid(row=1, column=2, columnspan=5, padx=10, sticky="w")
        CheckAttrP.grid(row=1, column=7, columnspan=2, sticky="w")
        # 3. Zeile
        CheckAttrV.grid(row=2, column=1, columnspan=2, sticky="w", pady=10)
        CheckAttrU.grid(row=2, column=3, columnspan=2, sticky="w")
        CheckAttrS.grid(row=2, column=5, columnspan=2)
        CheckAttrL.grid(row=2, column=7, columnspan=2, sticky="w")
        # 4. Zeile
        TextFav1.grid(row=3, column=1, pady=10)
        TextFav2.grid(row=3, column=3)
        TextFav3.grid(row=3, column=5)
        TextFav4.grid(row=3, column=7)
        EingabeFav1.grid(row=3, column=2, sticky="w")
        EingabeFav2.grid(row=3, column=4, sticky="w")
        EingabeFav3.grid(row=3, column=6, sticky="w")
        EingabeFav4.grid(row=3, column=8, sticky="w")
        # 5. Zeile
        ButtonSpeichern.grid(row=4, column=1, columnspan=4, pady=20, ipadx=18)
        ButtonAbbrechen.grid(row=4, column=5, columnspan=3, pady=20, ipadx=25)
        tk.Label(Fenster).grid(row=5, column=0, pady=1)

        EingabeNr.insert(0, prNum[Index[cp]])
        EingabeNr.select_range(0, tk.END)
        EingabeNr.focus_set()
        EingabeName.insert(0, vchName[Index[cp]])
        EingabeFav1.insert(0, favoriteIdxA[Index[cp]])
        EingabeFav2.insert(0, favoriteIdxB[Index[cp]])
        EingabeFav3.insert(0, favoriteIdxC[Index[cp]])
        EingabeFav4.insert(0, favoriteIdxD[Index[cp]])

        ButtonSpeichern.bind("<Return>", Eintrag_Aendern)
        ButtonAbbrechen.bind("<Return>", lambda event: Fenster_Schliessen(Fenster))
        Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Datei_Schreiben(dname):

    global Editiert

    # Alle Pufferzeilen aktualisieren
    a = idxDTV + 1      # Zeiger auf ersten Eintrag: <CHANNEL> <DTV> <ITEM>
    i = 0
    while Puffer[a+i*42] != "</DTV>\n":
        i += 1
        Puffer[a+(i*42-41)] = "<prNum>"         + prNum[i-1]         + "</prNum>\n"
        Puffer[a+(i*42-8)]  = "<vchName>"       + vchName[i-1]       + "</vchName>\n"
        Puffer[a+(i*42-11)] = "<isScrambled>"   + isScrambled[i-1]   + "</isScrambled>\n"
        Puffer[a+(i*42-18)] = "<isInvisable>"   + isInvisable[i-1]   + "</isInvisable>\n"
        Puffer[a+(i*42-16)] = "<isSkipped>"     + isSkipped[i-1]     + "</isSkipped>\n"
        Puffer[a+(i*42-17)] = "<isBlocked>"     + isBlocked[i-1]     + "</isBlocked>\n"
        Puffer[a+(i*42-14)] = "<isDeleted>"     + isDeleted[i-1]     + "</isDeleted>\n"
        Puffer[a+(i*42-26)] = "<favoriteIdxA>"  + favoriteIdxA[i-1]  + "</favoriteIdxA>\n"
        Puffer[a+(i*42-25)] = "<favoriteIdxB>"  + favoriteIdxB[i-1]  + "</favoriteIdxB>\n"
        Puffer[a+(i*42-24)] = "<favoriteIdxC>"  + favoriteIdxC[i-1]  + "</favoriteIdxC>\n"
        Puffer[a+(i*42-23)] = "<favoriteIdxD>"  + favoriteIdxD[i-1]  + "</favoriteIdxD>\n"
        Puffer[a+(i*42-28)] = "<mapAttr>"       + mapAttr[i-1]       + "</mapAttr>\n"
        Puffer[a+(i*42-4)]  = "<isUserSelCHNo>" + isUserSelCHNo[i-1] + "</isUserSelCHNo>\n"

    # alle Listenelemente mit gesetztem Löschattribut entfernen
    for i in range (i, 0, -1):         # von hinten nach vorne arbeiten!!
        if isDeleted[i-1] == "1":
            # 24 Listenelemente löschen
            del prNum[i-1], minorNum[i-1], original_network_id[i-1], transport_id[i-1]
            del service_id[i-1], serviceType[i-1], frequency[i-1], mapAttr[i-1]
            del favoriteIdxA[i-1], favoriteIdxB[i-1], favoriteIdxC[i-1], favoriteIdxD[i-1]
            del favoriteIdxE[i-1], favoriteIdxF[i-1], favoriteIdxG[i-1], favoriteIdxH[i-1]
            del isInvisable[i-1], isBlocked[i-1], isSkipped[i-1], isDeleted[i-1]
            del isScrambled[i-1], vchName[i-1], isUserSelCHNo[i-1], videoStreamType[i-1]
            # 42 Zeilen aus Puffer löschen
            for j in range(42, 0, -1):
                del Puffer[a+i*42-42]

    # aktualisierten Puffer in Datei schreiben
    with open(dname, "w", newline="\r\n") as Datei:     # \r\n = CRLF statt nur LF
        for i in range(0, len(Puffer), 1):
            Datei.write(Puffer[i])
        Datei.close()

    Editiert = False

###############################################################################################################
###############################################################################################################

def Alle_Anzeigen(event=None):

    Listen_Box.delete(0, tk.END) 
    Index.clear()
    for i in range(0, len(prNum), 1):
        Index.append(i)
        Channel_Zeile_Anzeigen(Index[i])
    Cursor_Anzeigen()
    Titelleiste_Anzeigen()
    Statusleiste_Anzeigen("Chronologisch")

###############################################################################################################

def SDTV_Anzeigen():

    Listen_Box.delete(0, tk.END) 
    Index.clear()
    for i in range(0, len(prNum), 1):
        if serviceType[i] == "1" or serviceType[i] == "22":
            Index.append(i)
            Channel_Zeile_Anzeigen(i)
    Cursor_Anzeigen()
    Statusleiste_Anzeigen("SD-TV")

###############################################################################################################

def HDTV_Anzeigen():

    Listen_Box.delete(0, tk.END) 
    Index.clear()
    for i in range(0, len(prNum), 1):
        if serviceType[i] == "17" or serviceType[i] == "25":
            Index.append(i)
            Channel_Zeile_Anzeigen(i)
    Cursor_Anzeigen()
    Statusleiste_Anzeigen("HD-TV")

###############################################################################################################

def UHDTV_Anzeigen():

    Listen_Box.delete(0, tk.END) 
    Index.clear()
    for i in range(0, len(prNum), 1):
        if serviceType[i] == "31" or serviceType[i] == "159":
            Index.append(i)
            Channel_Zeile_Anzeigen(i)
    Cursor_Anzeigen()
    Statusleiste_Anzeigen("UHD-TV")

###############################################################################################################

def Radio_Anzeigen():

    Listen_Box.delete(0, tk.END) 
    Index.clear()
    for i in range(0, len(prNum), 1):
        if serviceType[i] == "2" or serviceType[i] == "7" or serviceType[i] == "10":
            Index.append(i)
            Channel_Zeile_Anzeigen(i)
    Cursor_Anzeigen()
    Statusleiste_Anzeigen("Radio")

###############################################################################################################

def Favoriten_Anzeigen(fav):

    if   fav == 4:    favorite = favoriteIdxD
    elif fav == 3:    favorite = favoriteIdxC
    elif fav == 2:    favorite = favoriteIdxB
    else:             favorite = favoriteIdxA

    Index.clear()
    SortListe.clear()
    for i in range(0, len(prNum), 1):
        if int(favorite[i]) < 250:
            Index.append(i)
            SortListe.append(favorite[i])

    # Bubble Sort
    for j in range(len(Index)):
        tauschen = False
        for i in range(0, len(Index)-1, 1):
            if int(SortListe[i]) > int(SortListe[i+1]):
                SortListe[i], SortListe[i+1] = SortListe[i+1], SortListe[i]
                Index[i], Index[i+1]  = Index[i+1], Index[i]
                tauschen = True

    Listen_Box.delete(0, tk.END) 
    for i in range(0, len(Index), 1):
        Channel_Zeile_Anzeigen(Index[i])
    Cursor_Anzeigen()
    Statusleiste_Anzeigen("Favoriten {:d}".format(fav))

###############################################################################################################

def PayTV_Anzeigen():

    Listen_Box.delete(0, tk.END) 
    Index.clear()
    for i in range(0, len(prNum), 1):
        if isScrambled[i] == "1":
            Index.append(i)
            Channel_Zeile_Anzeigen(i)
    Cursor_Anzeigen()
    Statusleiste_Anzeigen("Pay-TV")

###############################################################################################################

def Sortieren_Namen():

    Index.clear()
    SortListe.clear()
    for i in range(0, len(prNum), 1):
        Index.append(i)
        SortListe.append(vchName[i])

    # Bubble Sort
    for j in range(len(prNum)):
        tauschen = False
        for i in range(0, len(prNum)-1, 1):
            if SortListe[i].lower() > SortListe[i+1].lower():
                SortListe[i], SortListe[i+1] = SortListe[i+1], SortListe[i]
                Index[i], Index[i+1]  = Index[i+1], Index[i]
                tauschen = True

    Listen_Box.delete(0, tk.END) 
    for i in range(0, len(prNum), 1):
        Channel_Zeile_Anzeigen(Index[i])
    Cursor_Anzeigen()
    Statusleiste_Anzeigen("Sortiert nach Name")

###############################################################################################################

def Sortieren_Nummer():

    Index.clear()
    SortListe.clear()
    for i in range(0, len(prNum), 1):
        Index.append(i)
        SortListe.append(prNum[i])

    # Bubble Sort
    for j in range(len(prNum)):
        tauschen = False
        for i in range(0, len(prNum)-1, 1):
            if int(SortListe[i]) > int(SortListe[i+1]):
                SortListe[i], SortListe[i+1] = SortListe[i+1], SortListe[i]
                Index[i], Index[i+1]  = Index[i+1], Index[i]
                tauschen = True

    Listen_Box.delete(0, tk.END) 
    for i in range(0, len(prNum), 1):
        Channel_Zeile_Anzeigen(Index[i])
    Cursor_Anzeigen()
    Statusleiste_Anzeigen("Sortiert nach Nummer")

###############################################################################################################

def Sortieren_Frequenz():

    Index.clear()
    SortListe.clear()
    for i in range(0, len(prNum), 1):
        Index.append(i)
        SortListe.append(frequency[i])

    # Bubble Sort
    for j in range(len(prNum)):
        tauschen = False
        for i in range(0, len(prNum)-1, 1):
            if int(SortListe[i]) > int(SortListe[i+1]):
                SortListe[i], SortListe[i+1] = SortListe[i+1], SortListe[i]
                Index[i], Index[i+1]  = Index[i+1], Index[i]
                tauschen = True

    Listen_Box.delete(0, tk.END) 
    for i in range(0, len(prNum), 1):
        Channel_Zeile_Anzeigen(Index[i])
    Cursor_Anzeigen()
    Statusleiste_Anzeigen("Sortiert nach Frequenz")

###############################################################################################################

def Filter_Suchen(event=None):

    def Sendernamen_Anzeigen(event=None):

        Suchbegriff = Eingabefeld.get()
        Fenster.destroy()

        Listen_Box.delete(0, tk.END) 
        Index.clear()
        for i in range(0, len(prNum), 1):
            if vchName[i].find(Suchbegriff) != -1:
                Index.append(i)
                Channel_Zeile_Anzeigen(i)
        Cursor_Anzeigen()
        Statusleiste_Anzeigen("Suche nach \"{:s}\"".format(Suchbegriff))


    Fenster = tk.Toplevel(Master)
    Fenster.title("Sendernamen suchen")
    Fenster.geometry("+370+160")
    Fenster.wm_attributes("-topmost", True)       # Fenster immer im Vordergrund halten
    Fenster.wait_visibility()
    Fenster.grab_set()                            # nur dieses Fenster aktiv schalten

    Eingabefeld = tk.Entry(Fenster, bd=4, width=30, font="Helvetica 12")
    ButtonSpeichern = tk.Button(Fenster, bd=3, text="Suchen", font="Helvetica 11", command=Sendernamen_Anzeigen)
    tk.Label(Fenster).pack(pady=1)
    Eingabefeld.pack(padx=50)
    ButtonSpeichern.pack(pady=17, ipadx=10)

    Eingabefeld.insert(0, "RTL")
    Eingabefeld.select_range(0, tk.END)
    Eingabefeld.focus_set()
    Eingabefeld.bind("<Return>", Sendernamen_Anzeigen)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################
###############################################################################################################

def ServiceInfo_Loeschen():

    aucSvcName.clear()
    usServiceID.clear()
    bVisibilityFlag.clear()
    bIsScramble.clear()
    usLCNValue.clear()
    ucServiceType.clear()
    usTPIndex.clear()

###############################################################################################################

def ServiceInfo_Laden():

    for a in range(0, len(Puffer)-1, 1):
        if Puffer[a] == "<astServiceInfo>\n":
            a += 1            # Zeiger auf "<ServCount0>"
            i = 0
            while Puffer[a+i*14] != "</astServiceInfo>\n":
                i += 1
                n = Puffer[a+(i*14-12)].find('</', 21)
                aucSvcName.append(Puffer[a+(i*14-12)][21:n])
                n = Puffer[a+(i*14-11)].find('</', 22)
                usServiceID.append(Puffer[a+(i*14-11)][22:n])
                n = Puffer[a+(i*14-10)].find('</', 26)
                bVisibilityFlag.append(Puffer[a+(i*14-10)][26:n])
                n = Puffer[a+(i*14-9)].find('</', 22)
                bIsScramble.append(Puffer[a+(i*14-9)][22:n])
                n = Puffer[a+(i*14-8)].find('</', 21)
                usLCNValue.append(Puffer[a+(i*14-8)][21:n])
                n = Puffer[a+(i*14-7)].find('</', 24)
                ucServiceType.append(Puffer[a+(i*14-7)][24:n])
                n = Puffer[a+(i*14-5)].find('</', 20)
                usTPIndex.append(Puffer[a+(i*14-5)][20:n])
        
###############################################################################################################

def ServiceInfo_Anzeigen(event=None):

    Fenster = tk.Toplevel(Master)
    Fenster.title("Service-Information")
    Fenster.geometry("+350+95")
    Fenster.wm_attributes("-topmost", True)   # Fenster immer im Vordergrund halten

    Scroll_Balken_V = tk.Scrollbar(Fenster, width=12)
    Scroll_Balken_H = tk.Scrollbar(Fenster, width=12, orient = tk.HORIZONTAL)
    Listen_Box = tk.Listbox(Fenster, width=65, height=40, yscrollcommand=Scroll_Balken_V.set, xscrollcommand = Scroll_Balken_H.set)
    Titelleiste = tk.Label(Fenster, text="  Pos  Sendername                     SID    V  P  LCN  STyp TPI", relief="sunken", anchor="w", font="Consolas 10")
    Scroll_Balken_V.config(command=Listen_Box.yview)
    Scroll_Balken_H.config(command=Listen_Box.xview)
    Listen_Box.config(bg=Hintergrund, fg=Vordergrund, font="Consolas 10")
    Titelleiste.pack(side="top", fill="x", padx=2, pady=1)
    Scroll_Balken_V.pack(side="right", fill="y", padx=1, pady=1)
    Scroll_Balken_H.pack(side="bottom", fill="x", padx=1, pady=1)
    Listen_Box.pack(fill="both", padx=2, pady=1, expand=True)

    ServiceInfo_Loeschen()
    ServiceInfo_Laden()
    if len(aucSvcName) == 0:
        Listen_Box.insert(tk.END, "  Keine Service-Informationen!")
    else:
        for i in range(0, len(aucSvcName), 1):
            Listen_Box.insert(tk.END, "{:5d}  {:30.30s} {:6s} {:2s} {:2s} {:5s} {:3s} {:3s}"\
                .format(i+1, aucSvcName[i], usServiceID[i], bVisibilityFlag[i], bIsScramble[i], usLCNValue[i], ucServiceType[i], usTPIndex[i]))
        Listen_Box.selection_set(0)
        Listen_Box.focus_set()

    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def TuningInfo_Loeschen():

    unFrequency.clear()
    unTSID.clear()
    unONID.clear()
    abwSymbolRate.clear()
    abwPolarization.clear() 
    abwCodeRate.clear()
    bwDVBS2.clear()
    abwModulationType.clear()
    bwDirection.clear()
    abwAnglePrec.clear()
    ucAngle.clear()
    ucNoOfServices.clear()
    usTPHandle.clear()

###############################################################################################################

def TuningInfo_Laden():

    for a in range(0, len(Puffer)-1, 1):
        if Puffer[a] == "<astTuningInfo>\n":
            a += 1           # Zeiger auf "<TPCount0>"
            i = 0
            while Puffer[a+i*17] != "</astTuningInfo>\n":
                i += 1
                n = Puffer[a+(i*17-16)].find('</', 22)
                unFrequency.append(Puffer[a+(i*17-16)][22:n])
                n = Puffer[a+(i*17-15)].find('</', 17)
                unTSID.append(Puffer[a+(i*17-15)][17:n])
                n = Puffer[a+(i*17-14)].find('</', 17)
                unONID.append(Puffer[a+(i*17-14)][17:n])
                n = Puffer[a+(i*17-13)].find('</', 24)
                abwSymbolRate.append(Puffer[a+(i*17-13)][24:n])
                n = Puffer[a+(i*17-12)].find('</', 26)
                abwPolarization.append(Puffer[a+(i*17-12)][26:n])
                n = Puffer[a+(i*17-11)].find('</', 22)
                abwCodeRate.append(Puffer[a+(i*17-11)][22:n])
                n = Puffer[a+(i*17-10)].find('</', 18)
                bwDVBS2.append(Puffer[a+(i*17-10)][18:n])
                n = Puffer[a+(i*17-9)].find('</', 28)
                abwModulationType.append(Puffer[a+(i*17-9)][28:n])
                n = Puffer[a+(i*17-7)].find('</', 22)
                bwDirection.append(Puffer[a+(i*17-7)][22:n])
                n = Puffer[a+(i*17-6)].find('</', 23)
                abwAnglePrec.append(Puffer[a+(i*17-6)][23:n])
                n = Puffer[a+(i*17-5)].find('</', 18)
                ucAngle.append(Puffer[a+(i*17-5)][18:n])
                n = Puffer[a+(i*17-4)].find('</', 25)
                ucNoOfServices.append(Puffer[a+(i*17-4)][25:n])
                n = Puffer[a+(i*17-3)].find('</', 21)
                usTPHandle.append(Puffer[a+(i*17-3)][21:n])

###############################################################################################################

def TuningInfo_Anzeigen(event=None):

    Fenster = tk.Toplevel(Master)
    Fenster.title("Tuning-Information")
    Fenster.geometry("+960+95")
    Fenster.wm_attributes("-topmost", True)   # Fenster immer im Vordergrund halten

    Scroll_Balken_V = tk.Scrollbar(Fenster, width=12)
    Scroll_Balken_H = tk.Scrollbar(Fenster, width=12, orient = tk.HORIZONTAL)
    Listen_Box = tk.Listbox(Fenster, width=64, height=40, yscrollcommand=Scroll_Balken_V.set, xscrollcommand = Scroll_Balken_H.set)
    Titelleiste = tk.Label(Fenster, text="  Pos  Freq   TSID  oNID SymRt Pol CR S2 Mod Dir Angel NOS TPH", relief="sunken", anchor="w", font="Consolas 10")
    Scroll_Balken_V.config(command=Listen_Box.yview)
    Scroll_Balken_H.config(command=Listen_Box.xview)
    Listen_Box.config(bg=Hintergrund, fg=Vordergrund, font="Consolas 10")
    Titelleiste.pack(side="top", fill="x", padx=2, pady=1)
    Scroll_Balken_V.pack(side="right", fill="y", padx=1, pady=1)
    Scroll_Balken_H.pack(side="bottom", fill="x", padx=1, pady=1)
    Listen_Box.pack(fill="both", padx=2, pady=1, expand=True)

    TuningInfo_Loeschen()
    TuningInfo_Laden()
    if len(unFrequency) == 0:
        Listen_Box.insert(tk.END, "  Keine Tuning-Informationen!")
    else:
        for i in range(0, len(unFrequency), 1):
            Listen_Box.insert(tk.END, "{:5d}  {:6s} {:5s} {:4s} {:6s}  {:2s} {:2s} {:2s} {:2s} {:2s} {:>3s},{:2s} {:3} {:4s}"\
                .format(i+1, unFrequency[i], unTSID[i], unONID[i], abwSymbolRate[i], abwPolarization[i], abwCodeRate[i], bwDVBS2[i],\
                abwModulationType[i], bwDirection[i], ucAngle[i], abwAnglePrec[i], ucNoOfServices[i], usTPHandle[i]))
        Listen_Box.selection_set(0)
        Listen_Box.focus_set()

    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def SatellitenInfo_Loeschen():

    SatelliteNameHex.clear()
    Angle.clear()
    AnglePrec.clear()
    DirEastWest.clear()

###############################################################################################################

def SatellitenInfo_Laden():

    for z in range(0, len(Puffer)-1, 1):
        if Puffer[z] == "<SatRecordInfo>\n":
            while Puffer[z] != "</SatRecordInfo>\n":
                z += 1
                if Puffer[z].find("<SatelliteNameHex") == 0:     # wenn gefunden
                    n = Puffer[z].find('</', 27)
                    SatelliteNameHex.append(Puffer[z][27:n])
                    n = Puffer[z+1].find('</', 16)
                    Angle.append(Puffer[z+1][16:n])
                    n = Puffer[z+2].find('</', 20)
                    AnglePrec.append(Puffer[z+2][20:n])
                    n = Puffer[z+3].find('</', 22)
                    DirEastWest.append(Puffer[z+3][22:n])

###############################################################################################################

def SatellitenInfo_Anzeigen(event=None):

    Fenster = tk.Toplevel(Master)
    Fenster.title("Satelliten-Information")
    Fenster.geometry("+730+160")
    Fenster.wm_attributes("-topmost", True)   # Fenster immer im Vordergrund halten

    Scroll_Balken_V = tk.Scrollbar(Fenster, width=12)
    Scroll_Balken_H = tk.Scrollbar(Fenster, width=12, orient = tk.HORIZONTAL)
    Listen_Box = tk.Listbox(Fenster, width=46, height=38, yscrollcommand=Scroll_Balken_V.set, xscrollcommand = Scroll_Balken_H.set)
    Titelleiste = tk.Label(Fenster, text="  Pos  Satellit                    Angel Dir", relief="sunken", anchor="w", font="Consolas 10")
    Scroll_Balken_V.config(command=Listen_Box.yview)
    Scroll_Balken_H.config(command=Listen_Box.xview)
    Listen_Box.config(bg=Hintergrund, fg=Vordergrund, font="Consolas 10")
    Titelleiste.pack(side="top", fill="x", padx=2, pady=1)
    Scroll_Balken_V.pack(side="right", fill="y", padx=1, pady=1)
    Scroll_Balken_H.pack(side="bottom", fill="x", padx=1, pady=1)
    Listen_Box.pack(fill="both", padx=2, pady=1, expand=True)

    SatellitenInfo_Loeschen()
    SatellitenInfo_Laden()
    if len(SatelliteNameHex) == 0:
        Listen_Box.insert(tk.END, "  Keine Satelliten-Informationen!")
    else:
        for i in range(0, len(SatelliteNameHex), 1):
            Listen_Box.insert(tk.END, "{:5d}  {:27.27s} {:>3s},{:2s} {:2s}"\
                .format(i+1, bytearray.fromhex(SatelliteNameHex[i]).decode(), Angle[i], AnglePrec[i], DirEastWest[i]))
        Listen_Box.selection_set(0)
        Listen_Box.focus_set()

    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def TransponderInfo_Loeschen():

    TransponderId.clear()
    Frequency.clear()
    Polarisation.clear()
    SymbolRate.clear()
    TransmissionSystem.clear()
    HomeTp.clear()

###############################################################################################################

def TransponderInfo_Laden():

    for a in range(0, len(Puffer)-1, 1):
        if Puffer[a] == "<TPList>\n":
            a += 2            # Zeiger auf "<TPRecord0>"
            i = 0
            while Puffer[a+i*8] != "</TPList>\n":
                i += 1
                n = Puffer[a+(i*8-7)].find('</', 24)
                TransponderId.append(Puffer[a+(i*8-7)][24:n])
                n = Puffer[a+(i*8-6)].find('</', 20)
                Frequency.append(Puffer[a+(i*8-6)][20:n])
                n = Puffer[a+(i*8-5)].find('</', 23)
                Polarisation.append(Puffer[a+(i*8-5)][23:n])
                n = Puffer[a+(i*8-4)].find('</', 21)
                SymbolRate.append(Puffer[a+(i*8-4)][21:n])
                n = Puffer[a+(i*8-3)].find('</', 29)
                TransmissionSystem.append(Puffer[a+(i*8-3)][29:n])
                n = Puffer[a+(i*8-2)].find('</', 17)
                HomeTp.append(Puffer[a+(i*8-2)][17:n])

###############################################################################################################

def TransponderInfo_Anzeigen():

    Fenster = tk.Toplevel(Master)
    Fenster.title("Transponder-Information")
    Fenster.geometry("+770+180")
    Fenster.wm_attributes("-topmost", True)   # Fenster immer im Vordergrund halten

    Scroll_Balken_V = tk.Scrollbar(Fenster, width=12)
    Scroll_Balken_H = tk.Scrollbar(Fenster, width=12, orient = tk.HORIZONTAL)
    Listen_Box = tk.Listbox(Fenster, width=36, height=35, yscrollcommand=Scroll_Balken_V.set, xscrollcommand = Scroll_Balken_H.set)
    Titelleiste = tk.Label(Fenster, text="  Pos  TPI  Freq  Pol SymRt  TS HTp", relief="sunken", anchor="w", font="Consolas 10")
    Scroll_Balken_V.config(command=Listen_Box.yview)
    Scroll_Balken_H.config(command=Listen_Box.xview)
    Listen_Box.config(bg=Hintergrund, fg=Vordergrund, font="Consolas 10")
    Titelleiste.pack(side="top", fill="x", padx=2, pady=1)
    Scroll_Balken_V.pack(side="right", fill="y", padx=1, pady=1)
    Scroll_Balken_H.pack(side="bottom", fill="x", padx=1, pady=1)
    Listen_Box.pack(fill="both", padx=2, pady=1, expand=True)

    TransponderInfo_Loeschen()
    TransponderInfo_Laden()
    if len(TransponderId) == 0:
        Listen_Box.insert(tk.END, "  Keine Transponder-Informationen!")
    else:
        for i in range(0, len(TransponderId), 1):
            Listen_Box.insert(tk.END, "{:5d}  {:4s} {:6s} {:2s} {:6s} {:2s} {:2s}"\
                .format(i+1, TransponderId[i], Frequency[i], Polarisation[i], SymbolRate[i], TransmissionSystem[i], HomeTp[i]))
        Listen_Box.selection_set(0)
        Listen_Box.focus_set()

    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def TransponderParameter_Loeschen():

    uwServiceStartIndex.clear()
    uwServiceEndIndex.clear()
    uwServiceCount.clear()
    nitVersion.clear()
    channelIndex.clear()
    frequency2.clear()
    original_network_id2.clear()
    transport_id2.clear()

###############################################################################################################

def TransponderParameter_Laden():

    for a in range(0, len(Puffer)-1, 1):
        if Puffer[a] == "<stTPRecParams>\n":
            a += 1            # Zeiger auf "<Record0>"
            i = 0
            while Puffer[a+i*34] != "</stTPRecParams>\n":
                i += 1
                n = Puffer[a+(i*34-33)].find('</', 30)
                uwServiceStartIndex.append(Puffer[a+(i*34-33)][30:n])
                n = Puffer[a+(i*34-32)].find('</', 28)
                uwServiceEndIndex.append(Puffer[a+(i*34-32)][28:n])
                n = Puffer[a+(i*34-31)].find('</', 25)
                uwServiceCount.append(Puffer[a+(i*34-31)][25:n])
                n = Puffer[a+(i*34-24)].find('</', 21)
                nitVersion.append(Puffer[a+(i*34-24)][21:n])
                n = Puffer[a+(i*34-23)].find('</', 23)
                channelIndex.append(Puffer[a+(i*34-23)][23:n])
                n = Puffer[a+(i*34-22)].find('</', 20)
                frequency2.append(Puffer[a+(i*34-22)][20:n])
                n = Puffer[a+(i*34-19)].find('</', 30)
                original_network_id2.append(Puffer[a+(i*34-19)][30:n])
                n = Puffer[a+(i*34-18)].find('</', 23)
                transport_id2.append(Puffer[a+(i*34-18)][23:n])

###############################################################################################################

def TransponderParameter_Anzeigen():

    Fenster = tk.Toplevel(Master)
    Fenster.title("Transponder-Parameter")
    Fenster.geometry("+710+140")
    Fenster.wm_attributes("-topmost", True)   # Fenster immer im Vordergrund halten

    Scroll_Balken_V = tk.Scrollbar(Fenster, width=12)
    Scroll_Balken_H = tk.Scrollbar(Fenster, width=12, orient = tk.HORIZONTAL)
    Listen_Box = tk.Listbox(Fenster, width=52, height=40, yscrollcommand=Scroll_Balken_V.set, xscrollcommand = Scroll_Balken_H.set)
    Titelleiste = tk.Label(Fenster, text="  Pos  TPI  Freq   sStart sEnde  SCt oNID TrID  NIT", relief="sunken", anchor="w", font="Consolas 10")
    Scroll_Balken_V.config(command=Listen_Box.yview)
    Scroll_Balken_H.config(command=Listen_Box.xview)
    Listen_Box.config(bg=Hintergrund, fg=Vordergrund, font="Consolas 10")
    Titelleiste.pack(side="top", fill="x", padx=2, pady=1)
    Scroll_Balken_V.pack(side="right", fill="y", padx=1, pady=1)
    Scroll_Balken_H.pack(side="bottom", fill="x", padx=1, pady=1)
    Listen_Box.pack(fill="both", padx=2, pady=1, expand=True)

    TransponderParameter_Loeschen()
    TransponderParameter_Laden()
    if len(channelIndex) == 0:
        Listen_Box.insert(tk.END, "  Keine TP-Parameter-Informationen!")
    else:
        for i in range(0, len(channelIndex), 1):
            Listen_Box.insert(tk.END, "{:5d}  {:4s} {:6s} {:6s} {:6s} {:3s} {:4s} {:5s} {:3s}"\
                .format(i+1, channelIndex[i], frequency2[i], uwServiceStartIndex[i], uwServiceEndIndex[i],\
                uwServiceCount[i], original_network_id2[i], transport_id2[i], nitVersion[i]))
        Listen_Box.selection_set(0)
        Listen_Box.focus_set()

    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################
###############################################################################################################

def Hilfe_Abkuerzungen(event=None):

    Fenster = tk.Toplevel(Master)
    Fenster.title("Abkürzungen")
    Fenster.geometry("+770+200")
    Fenster.wm_attributes("-topmost", True)   # Fenster immer im Vordergrund halten

    Text_Fenster = tk.Text(Fenster, width=35, height=33, pady=10, padx=10)
    Text_Fenster.config(bg=Hintergrund, fg=Vordergrund, font="Consolas 10", wrap="none")
    Text_Fenster.pack(fill="both", padx=3, pady=3, expand=True)

    Text_Fenster.configure(state="normal")
    Text_Fenster.delete("1.0", tk.END)
    Text_Fenster.insert(tk.END, "\n   Angel =  Winkel\n")
    Text_Fenster.insert(tk.END, "   CR    =  Code-Rate\n")
    Text_Fenster.insert(tk.END, "   Dir   =  Ausrichtung (West/Ost)\n")
    Text_Fenster.insert(tk.END, "   Fav   =  Favoriten\n")
    Text_Fenster.insert(tk.END, "   Freq  =  Frequenz\n")
    Text_Fenster.insert(tk.END, "   HTp   =  Home-Tp\n")
    Text_Fenster.insert(tk.END, "   L     =  Löschen\n")
    Text_Fenster.insert(tk.END, "   LCN   =  LCN-Value\n")
    Text_Fenster.insert(tk.END, "   mNr   =  minor Nummer\n")
    Text_Fenster.insert(tk.END, "   Mod   =  Modulation\n")
    Text_Fenster.insert(tk.END, "   NID   =  Netzwerk-ID\n")
    Text_Fenster.insert(tk.END, "   NIT   =  NIT-Version\n")
    Text_Fenster.insert(tk.END, "   NOS   =  Number of services\n")
    Text_Fenster.insert(tk.END, "   oNID  =  original Netzwerk-ID\n")
    Text_Fenster.insert(tk.END, "   P     =  Pay-TV (verschlüsselt)\n")
    Text_Fenster.insert(tk.END, "   Pol   =  Polarisation\n")
    Text_Fenster.insert(tk.END, "   Pos   =  Position\n")
    Text_Fenster.insert(tk.END, "   S     =  Sperren\n")
    Text_Fenster.insert(tk.END, "   S2    =  DVBS2\n")
    Text_Fenster.insert(tk.END, "   SCt   =  Service-Count\n")
    Text_Fenster.insert(tk.END, "   SID   =  Service-ID\n")
    Text_Fenster.insert(tk.END, "   STyp  =  Service-Typ\n")
    Text_Fenster.insert(tk.END, "   SymRt =  Symbolrate\n")
    Text_Fenster.insert(tk.END, "   TPH   =  TP-Handle\n")
    Text_Fenster.insert(tk.END, "   TPI   =  Transponder-Index\n")
    Text_Fenster.insert(tk.END, "   TrID  =  Transport-ID\n")
    Text_Fenster.insert(tk.END, "   TS    =  Transmission-System\n")
    Text_Fenster.insert(tk.END, "   TSID  =  Transponder-ID\n")
    Text_Fenster.insert(tk.END, "   U     =  Überspringen\n")
    Text_Fenster.insert(tk.END, "   V     =  Verstecken\n")
    Text_Fenster.insert(tk.END, "   VST   =  Videostream-Typ\n")
    Text_Fenster.configure(state="disabled")

    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Hilfe_Ueber():

    def Laufzeile():

        if Laufzeile.Zaehler < 150:
            Laufzeile.Zeichenkette = Laufzeile.Zeichenkette[1:] + Laufzeile.Zeichenkette[0]
            Lauftext.set(Laufzeile.Zeichenkette[0:41])
            Laufzeile.Zaehler += 1
            Fenster.after(70, Laufzeile)

    Fenster = tk.Toplevel(Master)
    Fenster.title("Über")
    Fenster.geometry("+720+350")
    Fenster.wm_attributes("-topmost", True)   # Fenster immer im Vordergrund halten
    Fenster.wait_visibility()
    Fenster.grab_set()                        # nur dieses Fenster aktiv schalten
    tk.Label(Fenster).pack()
    Zeile1 = tk.Label(Fenster, text="Channel View", font="Helvetica 20 bold")
    Zeile2 = tk.Label(Fenster, text="Version 1.00", font="Helvetica 12")
    Laufzeile.Zeichenkette = " +++++  Entwickelt von Woodstock  +++++  Dieses Programm wird\
 unter den Bedingungen der GNU General Public License veröffentlicht, Copyright (C) 2022. "
    Lauftext.set(Laufzeile.Zeichenkette[0:41])
    Zeile3 = tk.Label(Fenster, textvariable=Lauftext, font="Helvetica 12")
    Zeile1.pack(padx=110, pady=10) 
    Zeile2.pack(pady=10) 
    Zeile3.pack(pady=20)
    tk.Label(Fenster).pack()
    Laufzeile.Zaehler = 0
    Fenster.after(1500, Laufzeile)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Cursor_Anzeigen():

    if len(Index) == 0:
        Listen_Box.insert(tk.END, "  Keine Sender gefunden!")
    else:
        Listen_Box.selection_set(0)      # Scrollbalken auf erste Zeile
        Listen_Box.focus_set()


###############################################################################################################

def Titelleiste_Anzeigen():

    global Titeltext

    Titeltext.set("  Nr     mNr   Sendername                     STyp       Freq    SID    TSID   oNID  VST    P  V  U  S  L     Fav1 Fav2 Fav3 Fav4 Fav5 Fav6 Fav7 Fav8")

###############################################################################################################

def Channel_Zeile_Anzeigen(i):

    Listen_Box.insert(tk.END, "  {:6s} {:5s} {:30.30s} {:10s} {:7s} {:6s} {:6s} {:5s} {:3s} │  {:2s} {:2s} {:2s} {:2s} {:2s} │  {:4s} {:4s} {:4s} {:4s} {:4s} {:4s} {:4s} {:4s}"\
        .format(prNum[i], minorNum[i], vchName[i], servTypText[i], frequency[i], service_id[i], transport_id[i], original_network_id[i],\
        videoStreamType[i], isScrambled[i], isInvisable[i], isSkipped[i], isBlocked[i], isDeleted[i],\
        favoriteIdxA[i], favoriteIdxB[i], favoriteIdxC[i], favoriteIdxD[i], favoriteIdxE[i], favoriteIdxF[i], favoriteIdxG[i], favoriteIdxH[i]))

###############################################################################################################

def Statusleiste_Anzeigen(text):

    global Statustext

    Statustext.set(" {:6d} Sender   |   {:s}   |   {:s}".format(len(Index), text, os.path.basename(TLLDatei)))

###############################################################################################################

def Fenster_Schliessen(fenster):

    fenster.destroy()

###############################################################################################################

def Programm_Beenden(event=None):

    if Editiert:
        if message.askokcancel("Channel View", "\nEs wurden Einträge geändert. Sollen die Änderungen gespeichert werden?\n"):
            zeit = time.strftime("%Y%m%d%H%M%S")
            os.rename(TLLDatei, TLLDatei + "_" + zeit)
            Datei_Schreiben(TLLDatei)

    Master.destroy()

###############################################################################################################

Menuleiste = tk.Menu(Master, activebackground=Hintergrund, activeforeground=Vordergrund, font="Helvetica 11")
Menu_Datei = tk.Menu(Menuleiste, tearoff=0, activebackground=Hintergrund, activeforeground=Vordergrund, font="Helvetica 11")
Menu_Filter = tk.Menu(Menuleiste, tearoff=0, activebackground=Hintergrund, activeforeground=Vordergrund, font="Helvetica 11")
Menu_Filter_Favoriten = tk.Menu(Menu_Filter, tearoff=0, activebackground=Hintergrund, activeforeground=Vordergrund, font="Helvetica 11")
Menu_Filter_Sortieren = tk.Menu(Menu_Filter, tearoff=0, activebackground=Hintergrund, activeforeground=Vordergrund, font="Helvetica 11")
Menu_Tabellen = tk.Menu(Menuleiste, tearoff=0, activebackground=Hintergrund, activeforeground=Vordergrund, font="Helvetica 11")
Menu_Hilfe = tk.Menu(Menuleiste, tearoff=0, activebackground=Hintergrund, activeforeground=Vordergrund, font="Helvetica 11")

Menu_Datei.add_command(label=" Öffnen", command=Datei_Oeffnen, accelerator=" <Strg+O> ")
Menu_Datei.add_command(label=" Speichern", command=Datei_Speichern, accelerator=" <Strg+S> ")
Menu_Datei.add_command(label=" Speichern unter", command=Datei_Speichern_Unter)
Menu_Datei.add_separator()
Menu_Datei.add_command(label=" Editor (Experten)", command=Datei_Editor)
Menu_Datei.add_separator()
Menu_Datei.add_command(label=" Beenden", command=Programm_Beenden, accelerator=" <Strg+Q> ")
Menuleiste.add_cascade(label=" Datei ", menu=Menu_Datei, underline=1)

Menu_Filter.add_command(label=" SD-TV", command=SDTV_Anzeigen)
Menu_Filter.add_command(label=" HD-TV", command=HDTV_Anzeigen)
Menu_Filter.add_command(label=" UHD-TV", command=UHDTV_Anzeigen)
Menu_Filter.add_command(label=" Radio", command=Radio_Anzeigen)
Menu_Filter_Favoriten.add_command(label=" Favoriten 1", command=lambda: Favoriten_Anzeigen(1))
Menu_Filter_Favoriten.add_command(label=" Favoriten 2", command=lambda: Favoriten_Anzeigen(2))
Menu_Filter_Favoriten.add_command(label=" Favoriten 3", command=lambda: Favoriten_Anzeigen(3))
Menu_Filter_Favoriten.add_command(label=" Favoriten 4", command=lambda: Favoriten_Anzeigen(4))
Menu_Filter.add_cascade(label=" Favoriten ", menu=Menu_Filter_Favoriten, underline=1)
Menu_Filter.add_command(label=" Pay-TV", command=PayTV_Anzeigen)
Menu_Filter.add_separator()
Menu_Filter_Sortieren.add_command(label=" nach Namen", command=Sortieren_Namen)
Menu_Filter_Sortieren.add_command(label=" nach Nummer", command=Sortieren_Nummer)
Menu_Filter_Sortieren.add_command(label=" nach Frequenz", command=Sortieren_Frequenz)
Menu_Filter.add_cascade(label=" Sortieren", menu=Menu_Filter_Sortieren, underline=1)
Menu_Filter.add_command(label=" Suchen", command=Filter_Suchen, accelerator=" <F3> ")
Menu_Filter.add_separator()
Menu_Filter.add_command(label=" Alle anzeigen", command=Alle_Anzeigen, accelerator=" <F5> ")
Menuleiste.add_cascade(label=" Filter ", menu=Menu_Filter, underline=1)

Menu_Tabellen.add_command(label=" Service", command=ServiceInfo_Anzeigen, accelerator=" <F7> ")
Menu_Tabellen.add_command(label=" Tuning", command=TuningInfo_Anzeigen)
Menu_Tabellen.add_separator()
Menu_Tabellen.add_command(label=" Satelliten", command=SatellitenInfo_Anzeigen, accelerator=" <F9> ")
Menu_Tabellen.add_command(label=" Transponder", command=TransponderInfo_Anzeigen)
Menu_Tabellen.add_command(label=" TP-Parameter", command=TransponderParameter_Anzeigen)
Menuleiste.add_cascade(label=" Information ", menu=Menu_Tabellen, underline=1)

Menu_Hilfe.add_command(label=" Abkürzungen", command=Hilfe_Abkuerzungen, accelerator=" <F1> ")
Menu_Hilfe.add_separator()
Menu_Hilfe.add_command(label=" Über", command=Hilfe_Ueber)
Menuleiste.add_cascade(label=" Hilfe ", menu=Menu_Hilfe, underline=1)

Scroll_Balken_V = tk.Scrollbar(Master, width=12)
Scroll_Balken_H = tk.Scrollbar(Master, width=12, orient = tk.HORIZONTAL)
Listen_Box = tk.Listbox(Master, width=150, height=50, yscrollcommand=Scroll_Balken_V.set, xscrollcommand = Scroll_Balken_H.set)
Titelleiste = tk.Label(Master, textvariable=Titeltext, relief="sunken", anchor="w", font="Consolas 10")
Statusleiste = tk.Label(Master, textvariable=Statustext, relief="sunken", anchor="w", font="Helvetica 11")
Master.config(menu=Menuleiste)
Scroll_Balken_V.config(command=Listen_Box.yview)
Scroll_Balken_H.config(command=Listen_Box.xview)
Listen_Box.config(bg=Hintergrund, fg=Vordergrund, font="Consolas 10")
Titelleiste.pack(side="top", fill="x", padx=2, pady=1)
Statusleiste.pack(side="bottom", fill="x", padx=2, pady=1)
Scroll_Balken_V.pack(side="right", fill="y", padx=1, pady=1)
Scroll_Balken_H.pack(side="bottom", fill="x", padx=1, pady=1)
Listen_Box.pack(fill="both", padx=2, pady=1, expand=True)

Listen_Box.bind("<Double-Button-1>", Sender_Bearbeiten)
Listen_Box.bind("<Return>", Sender_Bearbeiten)
Listen_Box.bind("<Control-Key-o>", Datei_Oeffnen)
Listen_Box.bind("<Control-Key-s>", Datei_Speichern)
Listen_Box.bind("<Control-Key-q>", Programm_Beenden)
Listen_Box.bind("<F1>", Hilfe_Abkuerzungen)
Listen_Box.bind("<F3>", Filter_Suchen)
Listen_Box.bind("<F5>", Alle_Anzeigen)
Listen_Box.bind("<F7>", ServiceInfo_Anzeigen)
Listen_Box.bind("<F9>", SatellitenInfo_Anzeigen)

#----------------------------------------------------------------------

Titelleiste_Anzeigen()
Statusleiste_Anzeigen("")
Datei_Oeffnen()

Master.protocol("WM_DELETE_WINDOW", Programm_Beenden)

Master.mainloop()

###############################################################################################################
