import paramiko
import scp


class SSHConnector:

    def __init__(self, host, user, password):
        self.ssh_connection = self.connect_host(host, user, password)

    def connect_host(self, host, user, password):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, password=password)

        return ssh

    def copy_folder(self, source_path, destination_path):
        try:
            # Crear el comando para copiar la carpeta de origen a destino
            command = f"cp -r {source_path} {destination_path}"

            # Ejecutar el comando
            stdin, stdout, stderr = self.ssh_connection.exec_command(command)

            # Esperar a que termine la ejecución del comando
            stdout.channel.recv_exit_status()

            # Devuelvo True si se ha copiado correctamente
            return True
        except:
            # Devuelvo False si no ha podido ser copiado
            return False

    def remove_folder(self, folder_name):
        # Eliminar la carpeta si existe
        self.ssh_connection.exec_command(f'rm -r {folder_name}')

    def create_folder(self, folder_name):
        # Crear la carpeta especificada
        self.ssh_connection.exec_command('mkdir ' + folder_name)

    def rename_file(self, remote_path, new_name, ssh):
        rename_command = f"mv {remote_path}/* {remote_path}/{new_name}"
        self.ssh_connection.exec_command(rename_command)

    def transfer_file_or_folder_to_remote_location(self, source_path, remote_path):
        # Usamos SCP para transferir el archivo
        with scp.SCPClient(self.ssh_connection.get_transport()) as scp_client:
            scp_client.put(source_path, remote_path, recursive=True)

    def close_ssh_connection(self):
        self.ssh_connection.close()