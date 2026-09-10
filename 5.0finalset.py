biblioteca = {
    "BK01": {"titulo": "Python Pro", "autor": "Guido", "categorias": {"programacion", "backend"}},
    "BK02": {"titulo": "Bases de Datos", "autor": "Edgar", "categorias": {"datos", "backend", "sql"}},
    "BK03": {"titulo": "Frontend Moderno", "autor": "Sarah", "categorias": {"frontend", "web"}},
    "BK04": {"titulo": "Machine Learning", "autor": "Andrew", "categorias": {"inteligencia artificial", "datos", "python"}}
}

busqueda=input("Ingrese una categoría para buscar libros: ")
libros_encontrados = [libro for libro in biblioteca.values() if busqueda in libro["categorias"]]
if libros_encontrados:
    print(f"Libros encontrados en la categoría '{busqueda}':")
    for libro in libros_encontrados:
        print(f"  - {libro['titulo']} por {libro['autor']}")
else:
    print(f"No se encontraron libros en la categoría '{busqueda}'.")

for item in biblioteca.items():
    print(f"len({item[1]['titulo']}) = {len(item[1]['categorias'])}")

todas_las_categorias = set()
for libro in biblioteca.values():
    todas_las_categorias.update(libro["categorias"])
print(f"Todas las categorías: {', '.join(todas_las_categorias)}")
print(f"Categorías diferentes: {len(todas_las_categorias)}")
