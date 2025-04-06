from plexapi.server import PlexServer


class PlexConnector:

    def __init__(self, plex_url, plex_token):
        self.plex_connection = self.connect_to_plex(plex_url, plex_token)


    def connect_to_plex(self, plex_url, plex_token):

        # Conecta con el servidor de Plex
        return PlexServer(plex_url, plex_token)