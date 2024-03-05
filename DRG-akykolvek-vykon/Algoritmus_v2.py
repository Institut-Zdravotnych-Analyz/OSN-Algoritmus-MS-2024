def csvWrite(file, line, output):
    if len(output) == 0:
        output = ["ERROR"]
        print("ERROR: Line " + line + " does not have a code.")
    file.write(line + ";" + "~".join(output) + "\n")


def grouperMS(file):
    with open(file, 'r') as f:
        with open(file[:-4] + "_output.csv", "w") as fw:
            for line in f:
                if line[:4] == "id_h":
                    continue
                line = line.strip()
                data = line.split(";")

                data[5] = undot(data[5])
                data[6] = undot(data[6])

                output = set()

                if data[1] == "":
                    csvWrite(fw, line, ["ERROR"])
                    print("ERROR: Line " + line + " does not have an age.")
                    continue
                
                if int(data[1]) == 0 and int(data[2]) <= 28:
                    out = pril5(data[8], data[5], data[6], data[3], data[4])
                    output |= out

                
                if int(data[1]) <= 18 and data[8] != "" and data[5] != "":
                    out = pril6deti(data[8], data[5])
                    output |= out
                if int(data[1]) > 18 and data[8] != "" and data[5] != "":
                    out = pril6dosp(data[8], data[5])
                    output |= out

                
                if int(data[1]) <= 18 and data[6] != "":
                    out = pril7(data[6])
                    output |= out
                if int(data[1]) > 18 and data[6] != "":
                    out = pril8(data[6])
                    output |= out


                
                if int(data[1]) <= 18 and data[6] != "" and data[5] != "":
                    out = pril9deti1(data[6].split("~"), data[5])
                    output |= out
                if int(data[1]) > 18 and data[6] != "" and data[5] != "":
                    out = pril9dosp1(data[6].split("~"), data[5])
                    output |= out
                if int(data[1]) <= 18 and data[6] != "" and data[5] != "":
                    out = pril9deti2(data[6].split("~"), data[5].split("~"))
                    output |= out
                if int(data[1]) > 18 and data[6] != "" and data[5] != "":
                    out = pril9dosp2(data[6].split("~"), data[5].split("~"))
                    output |= out

                    
                
                if data[5] != "":
                    out = pril10(data[5])
                    output |= out
                    
                if int(data[1]) <= 18 and data[6] != "":
                    out = pril11deti(data[6].split("~"), data[7].split(","))
                    output |= out
                if int(data[1]) > 18 and data[6] != "":
                    out = pril11dosp(data[6].split("~"), data[7].split(","))
                    output |= out
                    
                if int(data[1]) <= 18 and data[6] != "":
                    out = pril12(data[6].split("~"))
                    output |= out
                    
                if int(data[1]) > 18 and data[6] != "":
                    out = pril13(data[6].split("~"))
                    output |= out
                    
                if int(data[1]) <= 18 and data[5] != "":
                    out = pril14(data[5].split("~")[0])
                    output |= out
                    
                if int(data[1]) > 18 and data[5] != "":
                    out = pril15(data[5].split("~")[0])
                    output |= out

                if data[5] != "":
                    out = pril16(data[5].split("~"))
                    output |= out
                csvWrite(fw, line, output)


def undot(diag):
    return diag.replace(".", "").replace("*", "")


def pril5def(diag, vyk, hmot, upv, kriterium):
    with open("Prilohy/p05_tab_krit_def.csv", "r", errors = "ignore") as pr:
        check = [0, -1]
        for line in pr:
            line = line.split(";")
            if line[0] == "kriterium":
                continue
            if line[0] == kriterium:
                if line[1] == "2" and check[1] == -1:
                    check[1] = 0
                if line[2] == "UPV>":
                    if int(upv) >= int(line[3]):
                        check[int(line[1])-1] = 1
                elif line[2] == "hmot<":
                    if int(hmot) <= int(line[3]):
                        check[int(line[1])-1] = 1
                elif line[2] == "dg":
                    for d in diag.split("~"):
                        if d[:len(line[2])] == line[2]:
                            if check[int(line[1])-1] == 0 and line[5] == 2:
                                check[int(line[1])-1] = 8
                            else:
                                check[int(line[1])-1] = 1
                            break
                elif line[2] == "vyk":
                    for v in vyk.split("~"):
                        if v.split("&")[0].lower() == line[3].lower():
                            check[int(line[1])-1] = 1
                            break
                else:
                    print("Zla tabulka p05_tab_krit_def.csv")
            if check[0] != 0 and check[1] != 0:
                return True
        return False

def pril5(drg, diag, vyk, hmot, upv):
    with open("Prilohy/p05_tab_DRG_krit_nov.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "DRG":
                continue
            if line[0] == drg[:len(line[0])] or line[0][1] == "A":
                if line[1] == "":
                    out.add(line[2])
                elif pril5def(diag, vyk, hmot, upv, line[1]):
                    out.add(line[2])
        return out
 



def pril6def(diag, skdg):
    with open("Prilohy/p06_tab_skdg_def.csv", "r", errors = "ignore") as pr:
        for line in pr:
            line = line.split(";")
            if line[0] == "skdg":
                continue
            if line[0] == skdg:
                zoz = line[1].strip().split(",")
                for z in zoz:
                    r = z.split("-")
                    if len(r) == 1:
                        for d in diag.split("~"):
                            if d[:len(z)] == z:
                                return True
                    elif len(r[0]) == len(r[1]):
                        for d in diag.split("~"):
                            if d[:len(r[0])] >= r[0] and d[:len(r[1])] <= r[1]:
                                return True
                    else:
                        print("Problem v prilohe p06_tab_skdg_def.csv")
                        print("Sposob zapisu diagnoz nie je implementovany")
        return False


def pril6deti(drg, diag):
    with open("Prilohy/p06_tab_DRG_skdg_deti.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "DRG":
                continue
            if line[0] == drg[:len(line[0])]:
                if line[1] == "":
                    out.add(line[2])
                elif pril6def(diag, line[1]):
                    out.add(line[2])
        return out

def pril6dosp(drg, diag):
    with open("Prilohy/p06_tab_DRG_skdg_dosp.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "DRG":
                continue
            if line[0] == drg[:len(line[0])]:
                if line[1] == "":
                    out.add(line[2])
                elif pril6def(diag, line[1]):
                    out.add(line[2])
        return out




def pril78def(vvyk, kod, subor):
    with open(subor, "r", errors = "ignore") as pr:
        for line in pr:
            line = line.split(";")
            if line[0] == "kodVVyk":
                continue
            if line[2] == kod:
                for v in vvyk:
                    if v.split("&")[0] == line[0]:
                        return True
        return False


def pril7(vyk):
    vyk = vyk.split("~")
##    hvyk = vyk[0]
##    vvyk = vyk[1:]
    with open("Prilohy/p07_tab_hvyk_skvvyk_deti.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "kodHVyk":
                continue
            for v in range(len(vyk)):
                vvyk = vyk[:v] + vyk[v+1:]
                hvyk = vyk[v]
                if undot(line[0]) == hvyk.split("&")[0]:
                    if pril78def(vvyk, line[2], "Prilohy/p07_tab_skvvyk_deti_def.csv"):
                        out.add(line[3])
                        break
        return out



def pril8(vyk):
    vyk = vyk.split("~")
##    hvyk = vyk[0]
##    vvyk = vyk[1:]
    with open("Prilohy/p08_tab_hvyk_skvvyk_dosp.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "kodHVyk":
                continue
            for v in range(len(vyk)):
                vvyk = vyk[:v] + vyk[v+1:]
                hvyk = vyk[v]
                if undot(line[0]) == hvyk.split("&")[0]:
                    if pril78def(vvyk, line[2], "Prilohy/p08_tab_skvvyk_dosp_def.csv"):
                        out.add(line[3])
                        break
        return out



def pril9extra(diag, kod, ext):
    with open("Prilohy/p" + ext[0] + "_tab_hdg_" + ext[1] + ".csv", "r", errors = "ignore") as pr:
        for line in pr:
            line = line.split(";")
            if line[0] == "KodHDg":
                continue
            if line[3] == kod:
                for d in diag:
                    if d[:len(line[0])] == line[0]:
                        return True
    return False



def pril9def(diag, Sk, ext):
    diag = diag.split("~")
    hdiag = diag[0]
    vdiag = diag[1:]
    with open("Prilohy/p09_tab_skdg_def.csv", "r", errors = "ignore") as pr:
        for line in pr:
            line = line.split(";")
            if line[0] == "SkDg":
                continue
            if line[0] == Sk:
                if line[1][0] == "a":
                    cdiag = diag
                elif line[1][0] == "h":
                    cdiag = [hdiag]
                elif line[1][0] == "v":
                    cdiag = vdiag
                else:
                    print(line[1])
                if line[2][:2] == "Vz":
                    kod = line[3].split("â€ž")[1].split("â€œ")[0]
                    if pril9extra(cdiag, kod, ext):
                        return True
                else:
                    for d in cdiag:
                        if d[:len(line[2])] == line[2]:
                            return True
        return False

def pril9deti1(vyk, diag):
    with open("Prilohy/p09_tab_hvyk_skdg_deti.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "kodHVyk":
                continue
            for v in vyk:
                if undot(line[0]) == v.split("&")[0]:
                    if pril9def(diag, line[2], ["14", "deti"]):
                        out.add(line[3])
                        break
        return out

def pril9dosp1(vyk, diag):
    with open("Prilohy/p09_tab_hvyk_skdg_dosp.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "kodHVyk":
                continue
            for v in vyk:
                if undot(line[0]) == v.split("&")[0]:
                    if pril9def(diag, line[2], ["15", "dosp"]):
                        out.add(line[3])
                        break
        return out




def pril92(diag, dgs):
    dgs = dgs.split(",")
    for d in range(len(dgs)):
        dgs[d] = dgs[d].strip()
    for d in dgs:
        if len(d) == 0:
            continue
        r = d.split("-")
        if len(r) == 1:
            for dia in diag:
                if dia[:len(d)] == d:
                    return True
        else:
            last = r[1].strip()
            base = r[0][:-len(last)]
            first = r[0][-len(last):]
            for dia in diag:
                if dia >= base + first and dia <= base + last:
                    return True
    


def pril9deti2(vyk, diag):
    with open("Prilohy/p09_tab_hvyk_dgs_deti.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "kodHVyk":
                continue
            for v in vyk:
                if undot(line[0]) == v.split("&")[0]:
                    if pril92(diag, line[4]):
                        out.add(line[2])
                        break
        return out

def pril9dosp2(vyk, diag):
    with open("Prilohy/p09_tab_hvyk_dgs_dosp.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "kodHVyk":
                continue
            for v in vyk:
                if undot(line[0]) == v.split("&")[0]:
                    if pril92(diag, line[4]):
                        out.add(line[2])
                        break
        return out




def pril10(diag):
    diag = diag.split("~")
    hdiag = diag[0]
    diag = diag[1:]
    if diag == []:
        return set()
    with open("Prilohy/p10_tab_hdg_vdg.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "kodHDg":
                continue
            if line[0] == hdiag:
                for d in diag:
                    if d == line[2]:
                        out.add(line[4])
                        break
        return out



def pril11deti(vyk, odb):
    with open("Prilohy/p11_tab_hvyk_odb_deti.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "kodOdb":
                continue
            for v in vyk:
                if undot(line[2]) == v.split("&")[0]:
                    for o in odb:
                        if o == line[0]:
                            out.add(line[4])
                            break
        return out


def pril11dosp(vyk, odb):
    with open("Prilohy/p11_tab_hvyk_odb_dosp.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "kodOdb":
                continue
            for v in vyk:
                if undot(line[2]) == v.split("&")[0]:
                    for o in odb:
                        if o == line[0]:
                            out.add(line[4])
                            break
        return out


                

def pril12(vyk):
    with open("Prilohy/p12_tab_hvyk_deti.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "kodHVyk":
                continue
            for v in vyk:
                if undot(line[0]) == v.split("&")[0]:
                    out.add(line[2])
                    break
        return out


def pril13(vyk):
    with open("Prilohy/p13_tab_hvyk_dosp.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "kodHVyk":
                continue
            for v in vyk:
                if undot(line[0]).lower() == v.split("&")[0].lower():
                    out.add(line[2])
                    break
        return out



def pril14(diag):
    with open("Prilohy/p14_tab_hdg_deti.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "kodHDg":
                continue
            if line[0] == diag:
                out.add(line[2])
        return out


def pril15(diag):
    with open("Prilohy/p15_tab_hdg_dosp.csv", "r", errors = "ignore") as pr:
        out = set()
        for line in pr:
            line = line.split(";")
            if line[0] == "kodHDg":
                continue
            if line[0] == diag:
                out.add(line[2])
        return out


def pril16(diags):
    with open("Prilohy/p16_tab_dgs.csv", "r", errors = "ignore") as pr:
        out = set()
        cur = ""
        num = 1
        ch = [0]
        for line in pr:
            line = line.split(";")
            if line[0] == "pocetKriterium" or line[0][-1] == "m":
                #Druha podmienka je tam lebo originalne boli prilohy zakodovane v UTF-8 with BOM namiesto len UTF-8, kde to davalo zopar extra symbolov na zaciatku suboru.
                continue
            if line[5] != cur:
                cur = line[5]
                num = int(line[0])
                ch = [0]*num
            if ch[int(line[1])-1] == 0:
                if line[2] == "dg":
                    if line[3] in diags:
                        ch[int(line[1])-1] = 1
                elif line[2] == "hdg":
                    if line[3] == diags[0]:
                        ch[int(line[1])-1] = 1
            if min(ch) == 1:
                out.add(cur)
                ch[0] = -1
        return out
            



print("Na spustenie programu, napiste 'grouperMS(\"nazov_suboru.csv\")' do konzoly.")

