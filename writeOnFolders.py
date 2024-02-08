import os

async def checkIfFolderExist(status_folder_name, facultad_folder_name):
    """
    Crea una carpeta siempre y cuando no exista

    :param status_folder_name: Nombre de carpeta como: Reutilizable, Nueva
    :type status_folder_name: str
    :param facultad_folder_name: Nombre de facultad
    :type facultad_folder_name: str
    :return: Crea la ruta en carpetas
    :rtype: str
    """

    await writeFolder(f"{status_folder_name}")
    await writeFolder(f"{status_folder_name}/{facultad_folder_name}")
    return f"{status_folder_name}/{facultad_folder_name}"


async def writeFolder(folder_name):
    """
    Lógica para crear una carpeta. No retorna valores.

    :param folder_name: Nombre de la carpeta
    :type folder_name: str
    """
    status = False;
    if not os.path.exists(folder_name):
        try:
            os.makedirs(folder_name)
            status = True
        except OSError as osE:
            status = False
    else:
        status = False
        #print(f"La carpeta ya existe")

