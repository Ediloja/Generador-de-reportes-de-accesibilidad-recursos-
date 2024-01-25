import asyncio
import pandas as pd
import dask.dataframe as dd
import time
import writePDF
from writeOnFolders import writeFolder, checkIfFolderExist
from weasyprint import HTML, CSS

async def get_summary(info_summary, comp_code):
    summary_values = {"resources_nm": 0, "cumply": 0,
                        "partially_complies": 0, 
                        "no_apply": 0, "not_cumply": 0}
    info_summary = info_summary.iloc[0:, :]

    unique_values = set()

    for index, row in info_summary.iterrows():
        if comp_code == row.iloc[2]:
            summary_values["resources_nm"] = row.iloc[3]
            summary_values["cumply"] = row.iloc[4]
            summary_values["not_cumply"] = row.iloc[5]
            summary_values["no_apply"] = row.iloc[6]
            summary_values["partially_complies"] = row.iloc[7]
            
            return summary_values
    
    return summary_values


async def set_value(row, summary_criteria):
    summary_criteria['rs_name'] = row.iloc[75]
    summary_criteria['url'] = row.iloc[79]
    for index in range(1, 13):
        summary_criteria[f'c{index}'] = row.iloc[80+index]
    
    return summary_criteria


async def set_data_criteria():
    summary_criteria = {"rs_name": "", "url": "",
                        "c1": "", "c2": "", "c3": "",
                        "c4": "", "c5": "", "c6": "",
                        "c7": "", "c8": "", "c9": "",
                        "c10": "", "c11": "", "c12": ""}
    return summary_criteria


async def write_report(path, filename, fileFin):
    pat = f"{path}/{filename}"
    print(pat)
    html_string = HTML(string=fileFin, base_url='./')
    css = CSS('files/styles.css')
    html_string.write_pdf(
    pat, stylesheets=[css])


async def read_excel_file():
    excel_file = "Enlistado de recursos COMPLETO.xlsx"
    sheet_1 = "Enlistado"
    sheet_2 = "Portadas"

    summcrit_table = ""
    status = True

    inicio_pandas = time.time()

    info = pd.read_excel(excel_file, sheet_name=sheet_1)
    info_summary = pd.read_excel(excel_file, sheet_name=sheet_2)
    columna = info["Etiquetado de archivos"]
    state_GDV_colum = info["Estado GDV"]
    facultad_colum = info["Facultad"]
    info = info.iloc[1:, :]

    unique_values = set()

    for index, row in info.iterrows():
        #await writeFolder(state_GDV[index])
        if (row.iloc[2] not in unique_values):
            summary_criteria = await set_data_criteria()

            unique_values.add(row.iloc[2])

            if (status == False):
                filename = banner_code + ".pdf"
                info_main = await writePDF.write_main_info(course_name, author_name, summary_val)
                fileFin = info_main + """<div class="container-table"> <h3 class="detail_h3">Detalle de recursos</h3>""" + summcrit_table +"""</div>""" + writePDF.footer()
                await write_report(path, filename, fileFin)
                

            banner_code = columna[index]
            course_name = row.iloc[3]
            author_name = row.iloc[5]

            criteria_summary = await set_value(row, summary_criteria)
            summcrit_table = ""
            summcrit_table = summcrit_table + await writePDF.summary_table(criteria_summary)

            summary_val = await get_summary(info_summary, row.iloc[2])
            path = await checkIfFolderExist(state_GDV_colum[index], facultad_colum[index])
        else: 
            status = False
            criteria_summary = await set_value(row, summary_criteria)
            summcrit_table = summcrit_table + await writePDF.summary_table(criteria_summary)
    

    filename = banner_code + ".pdf"
    info_main = await writePDF.write_main_info(course_name, author_name, summary_val)
    fileFin = info_main + """<div class="container-table"> <h3 class="detail_h3">Detalle de recursos</h3>""" + summcrit_table +"""</div>""" + writePDF.footer()
    await write_report(path, filename, fileFin)


    fin_pandas = time.time()
    tiempo_total_pandas = fin_pandas - inicio_pandas
    print(f"Tiempo final: {tiempo_total_pandas}")


asyncio.run(read_excel_file())