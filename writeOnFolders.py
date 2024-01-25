import os

async def checkIfFolderExist(state_folder_name, facultad_folder_name):
    await writeFolder(f"{state_folder_name}")
    await writeFolder(f"{state_folder_name}/{facultad_folder_name}")
    return f"{state_folder_name}/{facultad_folder_name}"

async def writeFolder(folder_name):
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

