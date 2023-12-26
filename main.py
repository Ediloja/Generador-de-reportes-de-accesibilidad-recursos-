import asyncio
import pandas as pd
import dask.dataframe as dd
import time
import writePDF
from weasyprint import HTML, CSS

async def get_summary(info_summary, comp_code):
    summary_values = {"resources_nm": 0, "cumply": 0,
                        "partially_complies": 0, 
                        "no_apply": 0, "not_cumply": 0}
    info_summary = info_summary.iloc[0:, :]

    unique_values = set()

    for index, row in info_summary.iterrows():
        if comp_code == row[2]:
            summary_values["resources_nm"] = row[3]
            summary_values["cumply"] = row[4]
            summary_values["not_cumply"] = row[5]
            summary_values["no_apply"] = row[6]
            summary_values["partially_complies"] = row[7]
            
            return summary_values
    
    return summary_values


async def set_value(row, summary_criteria):
    summary_criteria['rs_name'] = row[75]
    summary_criteria['url'] = row[79]
    for index in range(1, 13):
        summary_criteria[f'c{index}'] = row[80+index]
    
    return summary_criteria


async def set_data_criteria():
    summary_criteria = {"rs_name": "", "url": "",
                        "c1": "", "c2": "", "c3": "",
                        "c4": "", "c5": "", "c6": "",
                        "c7": "", "c8": "", "c9": "",
                        "c10": "", "c11": "", "c12": ""}
    return summary_criteria


async def write_report(filename, fileFin):
    html_string = HTML(string=fileFin, base_url='./')
    css = CSS('files/styles.css')
    html_string.write_pdf(
    filename, stylesheets=[css])


async def read_excel_file():
    excel_file = "Enlistado de recursos COMPLETO.xlsx"
    sheet_1 = "Enlistado"
    sheet_2 = "Portadas"

    summcrit_table = ""
    status = True

    inicio_pandas = time.time()

    info = pd.read_excel(excel_file, sheet_name=sheet_1)
    info_summary = pd.read_excel(excel_file, sheet_name=sheet_2)
    info = info.iloc[2:, :]

    unique_values = set()

    for index, row in info.iterrows():
        
        if row[2] not in unique_values:
            summary_criteria = await set_data_criteria()

            unique_values.add(row[2])

            if status == False:
                filename = "Reporte de accesibilidad de Recursos Educativos_" + banner_code + ".pdf"
                info_main = await writePDF.write_main_info(course_name, author_name, summary_val)
                fileFin = info_main + """<h3 class="detail_h3">Detalle de recursos</h3>""" + summcrit_table + writePDF.footer()
                await write_report(filename, fileFin)
                

            banner_code = row[2]
            course_name = row[3]
            author_name = row[5]

            criteria_summary = await set_value(row, summary_criteria)

            summcrit_table = summcrit_table + await writePDF.summary_table(criteria_summary)

            summary_val = await get_summary(info_summary, row[2])
            status = True
        else: 
            status = False
            criteria_summary = await set_value(row, summary_criteria)
            summcrit_table = summcrit_table + await writePDF.summary_table(criteria_summary)


    fin_pandas = time.time()
    tiempo_total_pandas = fin_pandas - inicio_pandas
    print(f"Tiempo final: {tiempo_total_pandas}")


asyncio.run(read_excel_file())