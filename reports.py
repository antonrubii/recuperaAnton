"""
Módulo de Generación de Informes PDF (Reports).

Permite recopilar datos de la persistencia SQL y formatearlos dinámicamente
en un archivo PDF legible usando la librería ReportLab.
"""
import os
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib import styles
from datetime import datetime
from conexion import Conexion


class Reports:
    """
    Clase estructurada para la maquetación y escritura de documentos analíticos imprimibles.
    """
    def __init__(self):
        # Crear carpeta de informes si no existe
        self.rootPath = "reports"
        if not os.path.exists(self.rootPath):
            os.makedirs(self.rootPath)

    def reportUsuarios(self):
        """Genera el informe PDF de usuarios ordenados por nombre"""
        try:
            # 1. Configuración del nombre del archivo
            fecha_hoy = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            nombre_pdf = f"informe_usuarios_{fecha_hoy}.pdf"
            path = os.path.join(self.rootPath, nombre_pdf)

            # 2. Crear el lienzo
            c = canvas.Canvas(path)

            # 3. Dibujar Cabecera
            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(300, 780, "LISTADO DE EMPLEADOS")

            c.setFont("Helvetica", 10)
            fecha_impresion = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.drawString(50, 750, f"Fecha de Impresión: {fecha_impresion}")
            c.line(50, 740, 550, 740)

            # 4. Títulos de columnas
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, 720, "Nombre")
            c.drawString(200, 720, "Email")
            c.drawString(400, 720, "Móvil")
            c.drawString(500, 720, "Tipo")
            c.line(50, 715, 550, 715)

            # 5. Obtener datos de la BD
            usuarios = Conexion.listadoUsuarios("Todos")

            y = 690
            c.setFont("Helvetica", 10)
            for user in usuarios:
                c.drawString(50, y, str(user[0]))   # Nombre
                c.drawString(200, y, str(user[2]))  # Email
                c.drawString(400, y, str(user[3]))  # Móvil
                c.drawString(500, y, str(user[4]))  # Tipo
                y -= 20

                if y < 50:
                    c.showPage()
                    y = 750

            c.save()
            os.startfile(path)

        except Exception as e:
            print("Error generando el PDF de usuarios:", e)

    def reportTareas(self):
        """Genera el informe PDF de tareas"""
        try:
            # Obtener datos de la base de datos
            datos = Conexion.listadoTareasPDF()

            # Nombre con fecha
            fecha_hoy = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            nombre_pdf = f"informe_tareas_{fecha_hoy}.pdf"
            path = os.path.join(self.rootPath, nombre_pdf)

            pdf = SimpleDocTemplate(path)
            elementos = []
            estilos = styles.getSampleStyleSheet()

            titulo = Paragraph("LISTADO DE TAREAS", estilos['Title'])
            fecha = Paragraph("Fecha de Impresión: " + datetime.now().strftime("%d/%m/%Y %H:%M"), estilos['Normal'])

            elementos.append(titulo)
            elementos.append(Spacer(1, 20))
            elementos.append(fecha)
            elementos.append(Spacer(1, 20))

            tabla = []
            cabecera = ["ID", "Cliente", "Empleado", "Servicio", "Horas", "Precio", "Estado", "Total"]
            tabla.append(cabecera)

            for t in datos:
                # --- CONTROL SEGURO DE VALORES NULOS (None) ---
                # Validamos que las posiciones 4 y 5 no sean vacías ni None antes de multiplicar
                horas = float(t[4]) if (len(t) > 4 and t[4] is not None and str(t[4]).strip() != "") else 0.0
                precio = float(t[5]) if (len(t) > 5 and t[5] is not None and str(t[5]).strip() != "") else 0.0

                total = horas * precio

                # Formateamos los campos de forma segura para evitar mostrar "None" en el PDF gráfico
                id_tarea = str(t[0]) if t[0] is not None else ""
                cliente = str(t[1]) if t[1] is not None else ""
                empleado = str(t[2]) if t[2] is not None else ""
                servicio = str(t[3]) if t[3] is not None else ""
                estado = str(t[6]) if (len(t) > 6 and t[6] is not None) else ""

                fila = [
                    id_tarea,
                    cliente,
                    empleado,
                    servicio,
                    f"{horas:.1f}",
                    f"{precio:.2f} €",
                    estado,
                    f"{total:.2f} €"
                ]
                tabla.append(fila)

            tablaPDF = Table(tabla)
            tablaPDF.setStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12)
            ])

            elementos.append(tablaPDF)
            pdf.build(elementos)

            os.startfile(path)
            print("PDF tareas generado con éxito.")

        except Exception as e:
            print("Error PDF:", e)