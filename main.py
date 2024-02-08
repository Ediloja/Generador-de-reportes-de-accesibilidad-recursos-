import asyncio
import pandas as pd
import dask.dataframe as dd
import time
import writePDF
from writeOnFolders import writeFolder, checkIfFolderExist
from weasyprint import HTML, CSS

async def get_summary(info_summary, comp_code):
    """
    Establece el resumen de un archivo. Valores como: Total de recursos,
        Cumple, No cumple, No aplica, Cumple parcialmente.

    :param info_summary: DataFrame con información de la hoja "Portadas"
    :type info_summary: Dataframe
    :param comp_code: Código de archivo, ejm 
    :type comp_code: str
    :return: Diccionario que contiene el resumen de un archivo de accesibilidad
    :rtype: dict
    """
    summary_values = {"resources_nm": 0, "cumply": 0,
                        "partially_complies": 0, 
                        "no_apply": 0, "not_cumply": 0}
    info_summary = info_summary.iloc[0:, :]

    ###
    tag_column = info_summary["Etiquetado de archivos"]
    trs_column = info_summary["Total recursos"]
    cum_column = info_summary["Cumple"]
    noc_column = info_summary["No cumple"]
    nap_column = info_summary["No aplica"]
    cmp_column = info_summary["Cumple parcialmente"]

    unique_values = set()

    for index, row in info_summary.iterrows():
        if comp_code == tag_column[index]:
            summary_values["resources_nm"] = trs_column[index]
            summary_values["cumply"] = cum_column[index]
            summary_values["not_cumply"] = noc_column[index]
            summary_values["no_apply"] = nap_column[index]
            summary_values["partially_complies"] = cmp_column[index]
            
            return summary_values
    
    return summary_values


async def set_value(info, row, index, summary_criteria):
    """
    Establece los valores de estado de cada criterio. Por ejemplo: Criterio-1 Cumple, Criterio2 No aplica, etc.

    :param info: DataFrame con información de la hoja "Enlistado"
    :type info: Dataframe
    :param row: Fila de un Dataframe
    :type row: obj
    :return: Diccionario con información de un recurso y su detalle sobre cada criterio
    :rtype: dict
    """
    resourcname_column = info["Nombre de recurso"]
    resourceURL_column = info["URL de recurso"]

    summary_criteria['rs_name'] = resourcname_column[index]
    summary_criteria['url'] = resourceURL_column[index]
    for index in range(1, 13):
        summary_criteria[f'c{index}'] = row.iloc[80+index]
    
    return summary_criteria


async def set_data_criteria():
    """
    Asigna el formato de para guardar las respuestas de excel y 
    devuelve como un diccionario.
    
    :return: Diccionario que contiene la estructura de como se almacena los criterios
    :rtype: dict
    """
    summary_criteria = {"rs_name": "", "url": "",
                        "c1": "", "c2": "", "c3": "",
                        "c4": "", "c5": "", "c6": "",
                        "c7": "", "c8": "", "c9": "",
                        "c10": "", "c11": "", "c12": ""}
    return summary_criteria


async def write_report(path, filename, fileFin):
    """
    Escribe el documento PDF con la información de accesibilidad de recursos
    
    :param path: Ruta de carpetas donde se guardará el archivo
    :type path: str
    :param filename: Nombre del archivo de reporte de accesibilidad
    :type filename: str
    :param fileFin: Contenido del reporte de accesibilidad
    :type fileFin: str
    """

    pat = f"{path}/{filename}"
    print(pat)
    html_string = HTML(string=fileFin, base_url='./')
    css = CSS('files/styles.css')
    html_string.write_pdf(
    pat, stylesheets=[css])


async def read_excel_file():
    """
    Contiene el proceso para buscar y asignar la información de un excel y apartir de ahí crear 
    el formato final que se escribirá en el reporte de accesibilidad (documento PDF)
    """

    excel_file = "Enlistado de recursos COMPLETO.xlsx"
    sheet_1 = "Enlistado"
    sheet_2 = "Portadas"

    summcrit_table = ""
    status = True

    inicio_pandas = time.time()

    info = pd.read_excel(excel_file, sheet_name=sheet_1)
    info_summary = pd.read_excel(excel_file, sheet_name=sheet_2)

    ###
    tag_column = info["Etiquetado de archivos"]
    nam_column = info["Nombre de Asignatura"]
    aut_column = info["Autor GDV"]

    state_GDV_colum = info["Estado GDV"]
    facultad_colum = info["Facultad"]
    info = info.iloc[0:, :]

    unique_values = set()

    for index, row in info.iterrows():
        #await writeFolder(state_GDV[index])
        if (tag_column[index] not in unique_values):
            summary_criteria = await set_data_criteria()

            unique_values.add(tag_column[index])

            if (status == False):
                filename = banner_code + ".pdf"
                info_main = await writePDF.write_main_info(course_name, author_name, summary_val)
                fileFin = info_main + """<div class="container-table"> <h3 class="detail_h3">Detalle de recursos</h3>""" + summcrit_table +"""</div>""" + writePDF.footer()
                await write_report(path, filename, fileFin)
                
            banner_code = tag_column[index]
            course_name = nam_column[index]
            author_name = aut_column[index]

            criteria_summary = await set_value(info, row, index, summary_criteria)
            summcrit_table = ""
            summcrit_table = summcrit_table + await writePDF.summary_table(criteria_summary)

            summary_val = await get_summary(info_summary, tag_column[index])
            path = await checkIfFolderExist(state_GDV_colum[index], facultad_colum[index])
        else: 
            status = False
            criteria_summary = await set_value(info, row, index, summary_criteria)
            summcrit_table = summcrit_table + await writePDF.summary_table(criteria_summary)
    

    filename = banner_code + ".pdf"
    info_main = await writePDF.write_main_info(course_name, author_name, summary_val)
    fileFin = info_main + """<div class="container-table"> <h3 class="detail_h3">Detalle de recursos</h3>""" + summcrit_table +"""</div>""" + writePDF.footer()
    await write_report(path, filename, fileFin)


    fin_pandas = time.time()
    tiempo_total_pandas = fin_pandas - inicio_pandas
    print(f"Tiempo final: {tiempo_total_pandas}")


asyncio.run(read_excel_file())