import myjdapi


class MyJDownloaderConnector:

    def __init__(self, user, password, device, app_key):
        self.user = user
        self.password = password
        self.device = device
        self.app_key = app_key
        self.jd_connection = None
        self.device_session = None
        self.connect_to_jdownloader()

    # CONEXION A JDOWLOADER ##########################

    def connect_to_jdownloader(self):
        self.jd_connection = myjdapi.Myjdapi()
        self.jd_connection.set_app_key(self.app_key)
        self.jd_connection.connect(self.user, self.password)

        # Obtener los dispositivos disponibles
        self.jd_connection.update_devices()

        # Obtenemos los datos del dispositivo especifico
        self.device_session = self.jd_connection.get_device(self.device)
        
    
    def reconnect_if_needed(self):
        # Verifica si la conexión está activa
        if not self.jd_connection.is_connected():
            print("Reconectando a JDownloader...")
            self.connect_to_jdownloader()
    
    # AÑADIR ENLACES ##########################

    # Añadir el enlace al LinkGrabber
    def add_link_to_linkgrabber(self, link):
        self.reconnect_if_needed()
        self.device_session.linkgrabber.add_links([link])
        print(f"Enlace añadido a LinkGrabber: {link}")


    # COMPROBAR ENLACES ##########################

    # Retornamos los enlaces de la pestaña downloads para ver que se hayan subido
    def check_download_links(self):
        self.reconnect_if_needed()
        return self.device_session.downloads.query_links()
        
    # Retornamos los enlaces de la pestaña downloads para ver que se hayan subido
    def check_linkgrabber_links(self):
        self.reconnect_if_needed()
        return self.device_session.linkgrabber.query_links()
    
    # LIMPIEZA DE ENLACES ##########################

    # Limpiar la pestaña downloads
    def cleanup_download_links(self):
        self.reconnect_if_needed()
        self.device_session.downloads.cleanup("DELETE_ALL", "REMOVE_LINKS_AND_RECYCLE_FILES", "ALL")
    
    # Limpiar el LinkGrabber
    def cleanup_linkgrabber(self):
        self.reconnect_if_needed()
        self.device_session.linkgrabber.cleanup("DELETE_ALL", "REMOVE_LINKS_AND_DELETE_FILES", "ALL")
        
    def full_cleanup(self):
        self.cleanup_download_links()
        self.cleanup_linkgrabber()

    