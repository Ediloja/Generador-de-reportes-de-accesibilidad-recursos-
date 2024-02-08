from weasyprint import HTML, CSS
from datetime import datetime

class PDF():
    def setHeader(self):
        """
        :return: Título del reporte de accesibilidad
        :rtype: str
        """

        header = '<br /><br /><p class="title">Reporte de accesibilidad recursos educativos digitales</strong></p>'
        return header 
    
    def set_mainInfo(self, course_name, teacher, summary_text):
        """
        Establece en código HTML el encabezado de un reporte de accesibilidad, esto incluye información
        general de curso (Nombre de la institución, nombre de la asignatura, Nombre del profesor, etc.)

        :param course_name: Nombre del curso
        :type course_name: str
        :param teacher: Nombre del profesor
        :type teacher: str
        :param summary_text: Texto de resumen
        :type summary_text: str
        :return: Información del encabezado de un reporte de accesibilidad
        :rtype: str
        """

        main_information = '''<div class="info_general"><p style="line-height: 1.5;"><strong>Nombre de la institución: </strong>Universidad Técnica Particular de Loja </br>
        <strong>Nombre de la asignatura: </strong>''' + str(course_name) + '''</br>
        <strong>Nombre del profesor responsable del metacurso: </strong>''' + str(teacher).title() + '''</br>
        <strong>Periodo académico: </strong> octubre 2023-febrero 2024 </br>
        <strong>Generado por: </strong> Ediloja Cía. Ltda. </br>
        <strong>Fecha de emisión del reporte: </strong>20-09-2023</p></div>
        <h3>Resumen general de cumplimiento</h3>
        <p class="summ_text">''' + str(summary_text) + '''</p>'''

        return main_information
    

    def set_resume(self, resource_sum):
        """
        Información parte del encabezado de un reporte de accesibilidad. Contiene el resumen en números
        de los recursos. Numero de recursos que cumplen, número de recursos que cumplen parcialmente, etc.

        :param resource_sum: sección que contiene información sobre el resumen de un reporte de accesibilidad de recursos
        :type resource_sum: str
        
        :return: Resumen de recursos de accesibilidad
        :rtype: str
        """

        main_information = f'''<div class="info_general"><p style="line-height: 1.5;">Número de recursos: {resource_sum["resources_nm"]} </br>
        Cumple (C): {resource_sum["cumply"]}</br>
        Cumple parcialmente (CP): {resource_sum["partially_complies"]}</br>
        No aplica (NA): {resource_sum["no_apply"]}</br>
        No cumple (NC): {resource_sum["not_cumply"]} </p></div>'''

        return main_information
    
    
    def details_of_resources(self, summary_criteria):
        """
        Establece la estructura de tabla en HTML sobre un recurso y el estado de cumplimiento de sus criterios
        (cumple, no aplica, cumple parcialmente, no cumple)

        :param summary_criteria: Diccionario con información de cada recurso
        :type summary_criteria: dic
        
        :return: Tabla con información de un recurso
        :rtype: str
        """

        summ_table = f'''<div class="div_table"><table>
            <caption><strong>Nombre de recurso:</strong> {summary_criteria["rs_name"]}</br>
                        <strong>URL:</strong> <a href="{summary_criteria["url"]}">{summary_criteria["url"]}</a></caption>
            <thead>
                <tr>
                    <th>*Criterios de calidad</th>
                    <th colspan="2">Definición didáctica Norma UNE 71362 y criterios de conformidad WCAG 2.1</th>
                    <th>Estado</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td colspan="4"><strong>Formato y diseño</strong></td>
                </tr>
                <tr>
                    <td rowspan="2"><strong>C1</strong></td>
                    <td rowspan="2">El diseño del recurso está bien organizado y es claro, conciso e intuitivo.</td>
                    <td><a href="https://www.w3.org/TR/WCAG21/#consistent-navigation">3.2.3 (AA)</a></td>
                    <td rowspan="2">{summary_criteria["c1"]}</td>
                </tr>
                <tr>
                    <td><a href="https://www.w3.org/TR/WCAG21/#consistent-identification">3.2.4 (AA)</a></td>
                </tr>
                <tr>
                    <td><strong>C2</strong></td>
                    <td>Hay consistencia entre la apariencia de los elementos funcionales (iconos, botones, etc.) y el resto de elementos de diseño a lo largo de todo el RED.</td>
                    <td><a href="https://www.w3.org/TR/WCAG21/#consistent-identification">3.2.4 (AA)</a></td>
                    <td>{summary_criteria["c2"]}</td>
                </tr>
                <tr>
                    <td colspan="4"><strong>Navegación</strong></td>
                </tr>
                <tr>
                    <td rowspan="2"><strong>C3</strong></td>
                    <td rowspan="2">El nombre de cada enlace es descriptivo, claro y diferente del resto de los enlaces. Los enlaces que llevan al mismo sitio utilizan el mismo texto descriptivo.</td>
                    <td><a href="https://www.w3.org/TR/WCAG21/#link-purpose-in-context">2.4.4 (A)</a></td>
                    <td rowspan="2">{summary_criteria["c3"]}</td>
                </tr>
                <tr>
                    <td><a href="https://www.w3.org/TR/WCAG21/#link-purpose-link-only">2.4.9 (AA)</a></td>
                </tr>
                <tr>
                    <td rowspan="2"><strong>C4</strong></td>
                    <td rowspan="2">Se proporcionan al menos dos mecanismos para localizar cada escenario de aprendizaje de la interfaz.</td>
                    <td><a href="https://www.w3.org/TR/WCAG21/#bypass-blocks">2.4.1 (A)</a></td>
                    <td rowspan="2">{summary_criteria["c4"]}</td>
                </tr>
                <tr>
                    <td><a href="https://www.w3.org/TR/WCAG21/#location">2.4.8 (AAA)</a></td>
                </tr>
                <tr>
                    <td rowspan="2"><strong>C5</strong></td>
                    <td rowspan="2">La interfaz proporciona tiempo ilimitado o suficiente para leer y usar el contenido.</td>
                    <td><a href="https://www.w3.org/TR/WCAG21/#no-timing">2.2.3 (AAA)</a></td>
                    <td rowspan="2">{summary_criteria["c5"]}</td>
                </tr>
                <tr>
                    <td><a href="https://www.w3.org/TR/WCAG21/#timing-adjustable">2.2.1 (A)</a></td>
                </tr>
                <tr>
                    <td colspan="4"><strong>Operabilidad</strong></td>
                </tr>
                <tr>
                    <td><strong>C6</strong></td>
                    <td>La operatividad es completa con teclado, ratón y cualquier otro dispositivo de entrada que se ofrezca, incluidos emuladores, activación por voz, interacción táctil, etc.</td>
                    <td><a href="https://www.w3.org/TR/WCAG21/#keyboard">2.1.1 (A)</a></td>
                    <td>{summary_criteria["c6"]}</td>
                </tr>
                <tr>
                    <td colspan="4"><strong>Contenido audiovisual</strong></td>
                </tr>
                <tr>
                    <td rowspan="2"><strong>C7</strong></td>
                    <td rowspan="2">Hay contraste suficiente entre el color de las imágenes y el color de fondo para que se vean bien.</td>
                    <td><a href="https://www.w3.org/TR/WCAG21/#contrast-minimum">1.4.3 (AA)</a></td>
                    <td rowspan="2">{summary_criteria["c7"]}</td>
                </tr>
                <tr>
                    <td><a href="https://www.w3.org/TR/WCAG21/#contrast-enhanced">1.4.6 (AAA)</a></td>
                </tr>
                <tr>
                    <td rowspan="3"><strong>C8</strong></td>
                    <td rowspan="3">Todos los contenidos audiovisuales (imágenes, gráficos, figuras, etc.) han de tener una descripción textual alternativa a la que se pueda acceder, bien de forma directa o bien a través de productos de apoyo.</td>
                    <td><a href="https://www.w3.org/TR/WCAG21/#non-text-content">1.1.1 (A)</a></td>
                    <td rowspan="3">{summary_criteria["c8"]}</td>
                </tr>
                <tr>
                    <td><a href="https://www.w3.org/TR/WCAG21/#images-of-text">1.4.5 (AA)</a></td>
                </tr>
                <tr>
                    <td><a href="https://www.w3.org/TR/WCAG21/#images-of-text-no-exception">1.4.9 (AAA)</a></td>
                </tr>
                <tr>
                    <td rowspan="2"><strong>C9</strong></td>
                    <td rowspan="2">El contenido no incluye efectos de destello con un umbral que pueda provocar ataques, espasmos o convulsiones.</td>
                    <td><a href="https://www.w3.org/TR/WCAG21/#three-flashes-or-below-threshold">2.3.1 (A)</a></td>
                    <td rowspan="2">{summary_criteria["c9"]}</td>
                </tr>
                <tr>
                    <td><a href="https://www.w3.org/TR/WCAG21/#three-flashes">2.3.2 (AA)</a></td>
                </tr>
                <tr>
                    <td colspan="4"><strong>Contenido textual</strong></td>
                </tr>
                <tr>
                    <td rowspan="2"><strong>C10</strong></td>
                    <td rowspan="2">El texto es legible o puede ajustarse su tamaño. El contenido textual de los recursos deberá presentarse con un mínimo de 18px.</td>
                    <td><a href="https://www.w3.org/TR/WCAG21/#resize-text">1.4.4 (AA)</a></td>
                    <td rowspan="2">{summary_criteria["c10"]}</td>
                </tr>
                <tr>
                    <td><a href="https://www.w3.org/TR/WCAG21/#visual-presentation">1.4.8 (AAA)</a></td>
                </tr>
                <tr>
                    <td rowspan="2"><strong>C11</strong></td>
                    <td rowspan="2">Existe un contraste adecuado entre el color de texto y el color de fondo para leerlo claramente y sin esfuerzo.</td>
                    <td><a href="https://www.w3.org/TR/WCAG21/#contrast-minimum">1.4.3 (AA)</a></td>
                    <td rowspan="2">{summary_criteria["c11"]}</td>
                </tr>
                <tr>
                    <td><a href="https://www.w3.org/TR/WCAG21/#contrast-enhanced">1.4.6 (AAA)</a></td>
                </tr>
                <tr>
                    <td><strong>C12</strong></td>
                    <td>Contraste suficiente entre los componentes de la interfaz de usuario, objetos gráficos y colores adyacentes.</td>
                    <td><a href="https://www.w3.org/TR/WCAG21/#non-text-contrast">1.4.11 (AA)</a></td>
                    <td>{summary_criteria["c12"]}</td>
                </tr>
            </tbody>
            </table><div/>'''

        return summ_table


def get_summText():
    """
    :return: Texto del resumen de un reporte de accesibilidad
    :rtype: str
    """

    return """Los criterios de accesibilidad considerados en este informe tienen 
            como base los estándares de calidad para recursos educativos digitales 
            señalados en la Norma UNE 71362:2020 y de los criterios de conformidad 
            de las pautas de accesibilidad al contenido web (WCAG 2.1)."""    
        

async def write_main_info(course_name, teacher, resource_sum):
    """
    Establece el encabezado del reporte de accesibilidad

    :param course_name: Nombre del curso
    :type course_name: str
    :param teacher: Nombre del profesor
    :type teacher: str
    :param resource_sum: Diccionario que contiene el resumen de un archivo de accesibilidad
    :type resource_sum: dict
    :return: Información de encabezado dell reporte de accesibilidad
    :rtype: str
    """

    pdf = PDF()
    title_info = pdf.setHeader()
    summary_text = get_summText()
    header = pdf.set_mainInfo(course_name, teacher, summary_text)

    resume = pdf.set_resume(resource_sum)

    return title_info + header + resume


async def summary_table(criteria_summary):
    """
    Establece el detalle de cada recurso y el estado sobre cada criterio

    :param criteria_summary: Diccionario con información de cada recurso
    :type criteria_summary: dic
    :return: Tabla de cada recurso
    :rtype: str
    """

    pdf = PDF()
    summary = pdf.details_of_resources(criteria_summary)
    return summary


def footer():
    """
    :return: Imagen QR
    :rtype: str
    """
    return """<img class="qr_code" src="files/qr-code_Ediloja.png"/>"""