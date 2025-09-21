class Zodiaco {
    constructor(dia, mes) {
        this.dia = dia;
        this.mes = mes;
    }

    nacimiento() {
        let dia = this.dia;
        let mes = this.mes;

        if ((mes === 3 && dia >= 21) || (mes === 4 && dia <= 19)) {
            return "ARIES";
        } else if ((mes === 4 && dia >= 20) || (mes === 5 && dia <= 20)) {
            return "TAURO";
        } else if ((mes === 5 && dia >= 21) || (mes === 6 && dia <= 20)) {
            return "GÉMINIS";
        } else if ((mes === 6 && dia >= 21) || (mes === 7 && dia <= 22)) {
            return "CÁNCER";
        } else if ((mes === 7 && dia >= 23) || (mes === 8 && dia <= 22)) {
            return "LEO";
        } else if ((mes === 8 && dia >= 23) || (mes === 9 && dia <= 22)) {
            return "VIRGO";
        } else if ((mes === 9 && dia >= 23) || (mes === 10 && dia <= 22)) {
            return "LIBRA";
        } else if ((mes === 10 && dia >= 23) || (mes === 11 && dia <= 21)) {
            return "ESCORPIO";
        } else if ((mes === 11 && dia >= 22) || (mes === 12 && dia <= 21)) {
            return "SAGITARIO";
        } else if ((mes === 12 && dia >= 22) || (mes === 1 && dia <= 19)) {
            return "CAPRICORNIO";
        } else if ((mes === 1 && dia >= 20) || (mes === 2 && dia <= 18)) {
            return "ACUARIO";
        } else if ((mes === 2 && dia >= 19) || (mes === 3 && dia <= 20)) {
            return "PISCIS";
        } else {
            return "FECHA INVÁLIDA";
        }
    }
}

// Programa principal
console.log("__DESCUBRE TU SIGNO ZODIACAL__");

// Para probarlo en consola, puedes cambiar estos valores:
let dia = parseInt(prompt("Ingresa el día de tu nacimiento: "));
let mes = parseInt(prompt("Ingresa el mes de tu nacimiento (1-12): "));

let signo = new Zodiaco(dia, mes);
console.log(`Tu signo zodiacal es: ${signo.nacimiento()}`);
