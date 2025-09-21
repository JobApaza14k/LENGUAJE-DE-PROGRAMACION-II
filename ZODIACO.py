class zodiaco:
    def __init__ (self, dia, mes):
        self.dia=dia
        self.mes=mes
    def nacimiento(self):
        if (mes==3 and dia>=21) or (mes == 4 and dia<=19):
            return "ARIES"
        elif (mes == 4 and dia>=20) or( mes== 5 and dia<=20):
            return "TAURO"
        elif (mes== 5 and dia>=21) or (mes == 6 and dia<=20):
            return "GEMINIS"
        elif (mes == 6 and dia >=21) or ( mes==7 and dia<=22):
            return "CANCER"
        elif (mes ==7 and dia>=23) or ( mes == 8 and dia<=22):
            return "LEO"
        elif (mes == 8 and dia>=23) or ( mes == 9 and dia<=22):
            return "VIRGO"
        elif (mes== 9 and dia>=23) or (mes == 10 and dia<=22):
            return "LIBRA"
        elif (mes == 10 and dia>=23) or (mes == 11 and dia<=21):
            return "ESCORPIO"
        elif (mes== 11 and dia>=22) or (mes==12 and dia<=21):
            return "SAGITARIO"
        elif (mes == 12 and dia>=22) or (mes==1 and dia<=19):
            return "CAPRICORNIO"
        elif (mes == 1 and dia >=20) or ( mes == 2 and dia<=18):
            return "ACUARIO"
        elif (mes == 2 and dia>=19) or (mes == 3 and dia<=20):
            return "PISCIS"
        else:
            return "fecha invalida"
            
print("__DESCUBRE TU SIGNO ZODIACAL__  ")
dia= int(input("ingrese el dia de tu nacimineto: "))
mes=int(input("ingrese el mes de tu naciomiento (1-12) : "))
signo = zodiaco(dia, mes)
print(f"tu signo zodiacal es: {signo.nacimiento()}")

