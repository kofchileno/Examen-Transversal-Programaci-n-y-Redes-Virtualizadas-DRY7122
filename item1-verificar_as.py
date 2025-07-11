# archivo: verificar_as.py

def verificar_as(asn):
    if 64512 <= asn <= 65534 or 4200000000 <= asn <= 4294967294:
        return "AS privado"
    elif 1 <= asn <= 64495 or 131072 <= asn <= 4199999999:
        return "AS público"
    else:
        return "AS no válido o reservado"

def main():
    try:
        asn = int(input("Ingrese el número de AS: "))
        resultado = verificar_as(asn)
        print(f"Resultado: {resultado}")
    except ValueError:
        print("Por favor, ingrese un número entero válido.")

if __name__ == "__main__":
    main()
