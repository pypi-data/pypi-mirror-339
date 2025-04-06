def filter_objects_by_condition(array, condition):
    """
    Filtra un array de objetos, devolviendo solo aquellos que cumplen con la condición dada.

    Parámetros:
    -----------
    array: list
        Lista de objetos (diccionarios) a filtrar.
    condition: function
        Una función que recibe un objeto y devuelve True si cumple con la condición, False de lo contrario.

        La condición debe ser una función lambda o cualquier función que tome un objeto (diccionario) como entrada
        y devuelva un valor booleano. Aquí hay ejemplos de cómo escribir condiciones:

        Ejemplos:
        ---------
        1. Condición para filtrar por una clave específica:
            Filtrar objetos donde 'season_of_the_year' sea 'summer':
            condition = lambda obj: obj.get('season_of_the_year') == "summer"

        2. Condición para filtrar por múltiples claves:
            Filtrar objetos donde 'season_of_the_year' sea 'summer' y 'year' sea 2024:
            condition = lambda obj: obj.get('season_of_the_year') == "summer" and obj.get('year') == 2024

    Retorna:
    --------
    list
        Lista de objetos que cumplen con la condición dada.
    """
    return [obj for obj in array if condition(obj)]