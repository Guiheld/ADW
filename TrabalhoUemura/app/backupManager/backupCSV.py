import os
from traceback import print_exception

import csv

from ..models import Usuarios

def atualizaBackupUsuarios():
    try:
        directory = os.path.dirname(__file__)  # puxa dir que ele esta
        filename = "backupUsuarios.csv"
        file_path = os.path.join(directory, filename) # faz o path absoluto

        usuarios = Usuarios.objects.all()

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'nome', 'email', 'senha'])

            for user in usuarios:
                writer.writerow([user.id_usuario, user.nome, user.email, user.senha])

        print(f"Backup feito: {filename}")
    except Exception as e:
        print_exception(type(e), e, e.__traceback__)

