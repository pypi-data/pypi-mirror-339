import sys
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class GoogleFirebaseConnector:
    """
       Clase para interactuar con una base de datos Firestore.

       Métodos:
       --------
       __init__(credentials_file_path: str):
           Inicializa la base de datos para poder usar las demás funciones.
       getDataByPath(path: str, target: str):
           Obtiene los datos desde la base de datos utilizando una ruta específica y un objetivo dentro del documento.
       setDataByPath(path: str, target: str, data: any):
           Sobrescribe los datos en un documento específico dentro de la base de datos siguiendo una ruta dada.
       """
    def __init__(self, creds_id: str, credentials_file_path: str):
        """
        Obtiene datos de un documento específico dentro de una base de datos siguiendo una ruta dada.
        :param credentials_file_path: Ruta hasta el archivo de las credenciales, ej. base-de-datos-f7431-firebase-adminsdk-4sa5k-fi919245c12.json"
        """
        self.credentials_file_path = credentials_file_path
        self.creds_id = creds_id
        self.db = self.init_database()

    def init_database(self):
        print(f"[FIREBASE]: Iniciando conexión con Firestore {self.creds_id}...\n", file=sys.stdout)

        firestore_creds = firebase_admin.initialize_app(
            credentials.Certificate(self.credentials_file_path),
            name=self.creds_id
        )
        return firestore.client(app=firestore_creds)

    # Enviando un path estilo así 'collection1/document1/collection2/document2' y enviando la key del interior del doc puedes recuperar datos
    def get_data_by_path(self, path: str, data_target: str):
        """
        Obtiene datos de un documento específico dentro de una base de datos siguiendo una ruta dada.

        La ruta debe especificar alternadamente colecciones y documentos, comenzando con una colección.
        Por ejemplo: 'collection1/document1/collection2/document2'.

        Parámetros:
        -----------
        path:str
            Ruta hasta la ubicación donde queremos obtener datos, e.g., 'anime/anime-by-letter/downloads/animelist'.
            La ruta debe tener un número par de elementos, alternando entre colecciones y documentos.
        data_target: str
            Clave dentro del documento desde la cual se obtendrán los datos. Debe ser un campo válido del documento final.

        Retorna:
        --------
        any
            Los datos asociados con la clave 'data_target' en el documento especificado.

        Excepciones:
        ------------
        ValueError
            - Si el número de elementos en la ruta es impar.
            - Si el documento final no existe o no contiene el campo 'data_target'.
        """

        path_splitted = path.split('/')

        # Verificar que el número de elementos en path_splited es par
        if len(path_splitted) % 2 != 0:
            raise ValueError(
                "[Error][get_data_by_path()]: El número de elementos en el path debe ser par para su correcto funcionamiento.")

        # Comenzar desde la primera colección especificada en el path
        ref = self.db.collection(path_splitted[0])

        # Recorrer el path en pares de (colección, documento)
        for i in range(1, len(path_splitted), 2):
            document_name = path_splitted[i]

            # Acceder al documento correspondiente
            ref = ref.document(document_name)

            # Sí hay más elementos en el path, acceder a la siguiente colección
            if i + 1 < len(path_splitted):
                ref = ref.collection(path_splitted[i + 1])

        # Obtener el documento final
        doc = ref.get().to_dict()

        # Verificar que el documento existe y contiene el target
        if doc is None or data_target not in doc:
            raise ValueError(f"[Error][get_data_by_path()]: El documento no contiene el objetivo '{data_target}' o no existe.")

        # Obtener los datos del data_target
        data = doc[data_target]

        # Imprimimos mensaje para avisar de que se está descargando
        print(f'[get_data_by_path()]: Descargando la información de "{path}/{data_target}"...\n', file=sys.stdout)

        # Devolver los datos.
        return data

    # Enviando un path estilo así 'collection1/document1/collection2' y enviando la key del interior del doc puedes recuperar la coleccion al completo
    def get_all_data_from_collection(self, path: str, data_target: str):
        """
        Obtiene datos de todos los documentos dentro de una colección específica.

        Parámetros:
        -----------
        path: str
            Ruta hasta la colección de la cual queremos obtener datos, e.g., 'anime/anime-by-letter/downloads'.
        data_target: str
            Clave dentro de los documentos desde la cual se obtendrán los datos. Debe ser un campo válido en los documentos.

        Retorna:
        --------
        list
            Lista con todos los datos asociados con la clave 'data_target' en los documentos de la colección especificada.

        Excepciones:
        ------------
        ValueError
            - Si la colección no existe.
            - Si los documentos no contienen el campo 'data_target'.
        """

        # Obtener la referencia a la colección
        collection_ref = self.db.collection(path)

        # Obtener todos los documentos de la colección
        docs = collection_ref.stream()
        data_list = []

        for doc in docs:
            doc_dict = doc.to_dict()

            # Verificar que el documento contiene el target
            if data_target in doc_dict:
                data = doc_dict[data_target]
                if isinstance(data, list):
                    data_list.extend(data)  # Si el dato es una lista, la extendemos
                else:
                    data_list.append(data)  # Si el dato no es una lista, simplemente lo añadimos
            else:
                print(
                    f"[Error][get_data_from_collection()]: El documento {doc.id} no contiene el objetivo '{data_target}'.")

        # Imprimimos mensaje para avisar de que se está descargando
        print(f'[get_all_data_from_collection()]: Descargando la información de "{path}/{data_target}"...\n',
              file=sys.stdout)

        return data_list

    # Aquí puedes setear datos en la base de datos
    def set_data_by_path(self, path: str, data_target: str, data: any):
        """
        Sobrescribe datos en un documento específico dentro de una base de datos siguiendo una ruta dada.

        La ruta debe especificar alternadamente colecciones y documentos, comenzando con una colección.
        Por ejemplo: 'collection1/document1/collection2/document2'.

        Parámetros:
        -----------
        path : str
            Ruta hasta la ubicación donde queremos sobrescribir datos, e.g., 'anime/anime-by-letter/downloads/animelist'.
            La ruta debe tener un número par de elementos, alternando entre colecciones y documentos.
        data_target : str
            Clave dentro del documento donde se sobrescribirán los datos. Debe ser un campo válido del documento final.
        data : any
            Los datos que se van a sobrescribir en el campo especificado por 'data_target'.

        Excepciones:
        ------------
        ValueError
            - Si el número de elementos en la ruta es impar.
        """
        path_splitted = path.split('/')

        # Verificar que el número de elementos en path_splitted es par
        if len(path_splitted) % 2 != 0:
            raise ValueError(
                "[Error][set_data_by_path()]: El número de elementos en el path debe ser par para su correcto funcionamiento.")

        # Comenzar desde la primera colección especificada en el path
        ref = self.db.collection(path_splitted[0])

        # Recorrer el path en pares de (colección, documento)
        for i in range(1, len(path_splitted), 2):
            document_name = path_splitted[i]

            # Acceder al documento correspondiente
            ref = ref.document(document_name)

            # Si hay más elementos en el path, acceder a la siguiente colección
            if i + 1 < len(path_splitted):
                ref = ref.collection(path_splitted[i + 1])

        # Crear o sobrescribir los datos en el documento final
        ref.set({data_target: data}, merge=True)

        # Imprimimos mensaje para avisar de que se está sobrescribiendo
        print(f'[set_data_by_path()]: Sobrescribiendo la información en "{path}/{data_target}"...\n', file=sys.stdout)

        # Confirmar la operación
        return f'Datos sobrescritos en {path}/{data_target}'

