import json

key = "1"

print("\n-------- BIENVENIDO-------- ")

def inicio_sesion():
    user = input("Ingrese su usuario: ")

    while True:
        password = input("Ingrese su contraseña: ")
        if password == key:
            print(f"Bienvenido, {user}")
            break
        else:
            input("Contraseña incorrecta. Por favor intente de nuevo.")

def cargar_datos(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def obtener_preferencias(tipo):
    print("\n---------PREFERENCIAS---------")
    generos = input("¿Qué generos le interesan? (separados en comas): ").lower()
    generos = [g.strip().lower() for g in generos.split(",") if g.strip()]

    persona = input(f"¿Hay algún {'autor' if tipo=="libro" else "director"} que te guste? (opcional): ").strip()
    persona = persona if persona else None

    año_min = input("¿Desde qué año te interesa? (opcional): ").strip()
    año_max = input("¿Hasta qué año? (opcional): ").strip()
    
    año_min = int(año_min) if año_min.isdigit() else None
    año_max = int(año_max) if año_max.isdigit() else None

    return generos, persona, año_min, año_max

def recomendar(items, tipo, generos_pref, persona_pref, año_min, año_max):
    recomendaciones = []

    for item in items:
        puntuacion = 0

        generos_item = [gen.lower() for gen in item["genero"]]
        if any(g in generos_item for g in generos_pref):
            puntuacion += 2

        if persona_pref:
            if persona_pref.lower() in item["autor" if tipo=="libro" else "director"].lower():
                puntuacion += 2

        if año_min and item["año"] < año_min:
            continue
        if año_max and item["año"] > año_max:
            continue

        if puntuacion > 0:
            recomendaciones.append((item))

    recomendaciones.sort(key=lambda x: x[1], reverse=True)
    return recomendaciones

def mostrar_recomendaciones(recomendaciones, tipo):
    print("\n------ RECOMENDACIONES ------")
    if not recomendaciones:
        print(f"No se encontraron {tipo} que coincidan con tus preferencias.")
        
    else:
        for item in recomendaciones:
            if tipo=="libro":
                print(f"\n{'NOMBRE':<25} | {'AUTOR':<20} | {'AÑO':<5}")
                print("-"*58)
                print(f"\n{item['titulo']:<25} | {item['autor']:<20} | {item['año']:<5}")
            else:
                print(f"\n{'NOMBRE':<25} | {'DIRECTOR':<20} | {'AÑO':<5}")
                print("-"*58)
                print(f"{item['titulo']:<25} | {item['director']:<20}, {item['año']:<5}")

def recomendaciones(tipo):
    archivo = "libros.json" if tipo=="libro" else "peliculas.json"
    items = cargar_datos(archivo)
    mostrar_recomendaciones(items,tipo)
    generos, persona, año_min, año_max = obtener_preferencias(tipo)
    recomendaciones = recomendar(items, generos, persona, año_min, año_max)
    mostrar_recomendaciones(recomendaciones)

def tipo():
    while True:
        eleccion = input("\n¿Qué recomendaciones desea? ¿Libro o Película? (escriba 'fin' para salir): ").lower().strip()
        if eleccion in ["libro","pelicula"]:
            recomendaciones(eleccion)
        elif eleccion == "fin":
            print("Gracias por usar el sistema. ¡Hasta luego!")
            break
        else:
            print("Entrada no válida. Por favor escriba 'libro', 'pelicula' o 'fin'.")

inicio_sesion()
tipo()