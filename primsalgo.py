"""
Martti Mourujärvi
2639437
marttimourujarvi@gmail.com
"""

import time
import random 
import sys, getopt
import bisect # Haetaan binäärihakualgoritmi

class Graph():

    def __init__(self, kaupungit, päämäärä):
        self.K = kaupungit # Kaupunkien lukumäärä
        self.P = päämäärä - 1
        self.graph = [[0 for column in range(kaupungit)] # Luodaan tyhjä matriisi korkeuksille
                        for row in range(kaupungit)]
        self.reitit = []
    
    def matalin_reitti(self, kaupunki, mst_asetettu):
        # Lisätään uuden kaupungin reitit tutkittavaksi
        reitit = self.graph[kaupunki]
        for i, reitti in enumerate(reitit):
            if reitti != 0 and not mst_asetettu[i]: # ei lisätä reittejä kaupunkeihin joihin on löydetty jo polku
                # Lisätään uusi reitti listaan kasvavassa järjestyksessä
                bisect.insort(self.reitit, (reitti, [i, kaupunki]))
        
        # Jos lyhyimmän reitin päämäärä on jo kerran löydetty, unohdetaan reitti
        while mst_asetettu[self.reitit[0][1][0]]:
            self.reitit.pop(0)
        
        lyhin_reitti = self.reitit[0]

        if not mst_asetettu[lyhin_reitti[1][0]]:
            # Tarkistetaan onko kaupunkia vielä löydetty, jos ei niin uusi kaupunki on löydetty
            uusi_kaupunki = self.reitit.pop(0)[1][0]

        return uusi_kaupunki, lyhin_reitti[0], lyhin_reitti[1][1]

    def reitin_selvitys(self, korkeudet, vanhemmat):
        # Löydetään reitti alkupisteestä maaliin ja samalla korkein kohta
        kaupunki = vanhemmat[self.P] # Aloitetaan reitin selvitys maalista
        reitti = []
        korkein_kohta = korkeudet[self.P] # määritetään reitin korkein kohta vertailemalla
        while kaupunki != -1:
            if korkein_kohta < korkeudet[kaupunki]:
                korkein_kohta = korkeudet[kaupunki]
            reitti.append(kaupunki + 1)
            kaupunki = vanhemmat[kaupunki]

        mahd_reitti = "Mahdollinen reitti: "
        # Aloitetaan reitin esittely alkupisteestä
        reitti.reverse()
        for kaupunki in reitti:
            mahd_reitti += str(kaupunki)
            mahd_reitti += " -> "
        mahd_reitti += str(self.P + 1)
        return korkein_kohta, mahd_reitti

        

    def prims_algo(self):
        # Luodaan arvot jotta löydetään pienin reuna aina tietyssä pisteessä.
        korkeudet = [None] * self.K # tallennetaan 
        parent = [None] * self.K
        mst_asetettu = [False] * self.K
        mst_asetettu[0] = True
        korkeudet[0] = 0
        parent[0] = -1 # ensimmäinen alkio on juuri
        kaupunki = 0
        while kaupunki < self.P:
            uusi, lyhyin_reitti, vanhempi = self.matalin_reitti(kaupunki, mst_asetettu)
            mst_asetettu[uusi] = True # Asetetaan kaupunki löydetyksi
            parent[uusi] = vanhempi #kaupunki # Nykyinen kaupunki on uuden kaupungin vanhempi
            korkeudet[uusi] = lyhyin_reitti
            kaupunki = uusi
            print("Tutkitaan seuraavaksi kaupunki: ", kaupunki + 1)
            print("######################################")
        
        # Korkeimman kohdan ja reitin selvitykseen
        korkein_kohta, reitti = self.reitin_selvitys(korkeudet, parent)
        print(reitti)
        print("--- Korkein kohta:", korkein_kohta, "---")
        
def main(folder, file):
    start_time = time.time()
    # Argumenttien käsittely, sekä kansio että tiedosto
    path = ""
    if folder == "-r":
        path = "graph_testdata/"
    elif folder == "-l":
        path = "graph_large_testdata/"
    tiedot = open(path + file, "r")
    fl = tiedot.readlines()
    # Päämäärän ja kaupunkien määrän tallennus
    päämäärä = int(fl[len(fl) - 1])
    kaupungit = int(fl[0].split()[0])
    # muodostetaan tieverkostosta matriisiesitys
    g = Graph(kaupungit, päämäärä)
    for i in range(1, len(fl) - 1):
        arvot = fl[i].split()
        # yhteen suuntaan
        g.graph[int(arvot[0]) - 1][int(arvot[1]) - 1] = int(arvot[2])
        # kahteen suuntaan
        g.graph[int(arvot[1]) - 1][int(arvot[0]) - 1] = int(arvot[2])
    g.prims_algo()
    print("--- %s seconds ---" % (time.time() - start_time)) 

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])




