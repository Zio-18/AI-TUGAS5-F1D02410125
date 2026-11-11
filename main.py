import json

file = open("kb_akademik.json", "r")
data = json.load(file)
file.close()

aturan = data["aturan"]

semua_jika = []
semua_maka = []

for r in aturan:
    semua_maka.append(r["maka"])
    for syarat in r["jika"]:
        if syarat not in semua_jika:
            semua_jika.append(syarat)

fakta_tanya = []
for f in semua_jika:
    if f not in semua_maka:
        fakta_tanya.append(f)

kesimpulan_akhir = []
for r in aturan:
    if r["maka"] not in semua_jika:
        kesimpulan_akhir.append(r["maka"])

print(data["judul"])
print("Jawab y/t.")

memori = []
nomor = 1
for f in fakta_tanya:
    jawab = input(str(nomor) + ". Apakah " + f + "? (y/t) > ")
    if jawab == "y" or jawab == "Y":
        memori.append(f)
    nomor = nomor + 1

print("")
if len(memori) > 0:
    print("Fakta awal: " + ", ".join(memori))
else:
    print("Fakta awal: tidak ada")
print("")

asal_aturan = {}
siklus = 1

while True:
    cocok = []
    for r in aturan:
        if r["maka"] not in memori:
            terpenuhi = False

            if r["mode"] == "dan":
                terpenuhi = True
                for s in r["jika"]:
                    if s not in memori:
                        terpenuhi = False

            elif r["mode"] == "atau":
                terpenuhi = False
                for s in r["jika"]:
                    if s in memori:
                        terpenuhi = True

            if terpenuhi == True:
                cocok.append(r)

    if len(cocok) == 0:
        print("Siklus " + str(siklus) + ": tidak ada aturan baru, berhenti")
        break

    r = cocok[0]
    memori.append(r["maka"])
    asal_aturan[r["maka"]] = r
    print("Siklus " + str(siklus) + ": " + r["id"] + " -> " + r["maka"])
    siklus = siklus + 1

print("")

hasil_akhir = []
for k in kesimpulan_akhir:
    if k in memori:
        hasil_akhir.append(k)

if len(hasil_akhir) > 0:
    print("Kesimpulan: " + ", ".join(hasil_akhir))
    print("Alasan:")
    for k in hasil_akhir:
        r = asal_aturan[k]
        syarat_dipakai = []
        for s in r["jika"]:
            if s in memori:
                syarat_dipakai.append(s)
        print("  " + k + " <- " + r["id"] + " (" + ", ".join(syarat_dipakai) + ")")

        for s in syarat_dipakai:
            if s in asal_aturan:
                r2 = asal_aturan[s]
                syarat_awal = []
                for s2 in r2["jika"]:
                    if s2 in memori:
                        syarat_awal.append(s2)
                print("    " + s + " <- " + r2["id"] + " (" + ", ".join(syarat_awal) + ")")
else:
    print("Kesimpulan: tidak ada")
    print("Alasan:")
    print("  fakta awal belum memenuhi aturan sampai kesimpulan akhir")

print("")
print("Catatan: " + data["batas"])