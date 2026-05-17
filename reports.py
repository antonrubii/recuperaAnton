import os
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table
from reportlab.platypus import Spacer
from reportlab.platypus import Paragraph
from reportlab.lib import colors
from reportlab.lib import styles
from datetime import datetime
from conexion import Conexion



class Reports:  # <--- ASEGÚRATE DE QUE SE LLAME ASÍ EXACTAMENTE
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

            # 5. Obtener datos de la BD (Mét0do de conexion.py)
            from conexion import Conexion
            usuarios = Conexion.listadoUsuarios("Todos")  # O el mét0do que creamos antes

            y = 690
            c.setFont("Helvetica", 10)
            for user in usuarios:
                # Ajusta los índices según tu SELECT [nombre, dni, email, movil, tipo]
                c.drawString(50, y, str(user[0]))  # Nombre
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
            print("Error generando el PDF:", e)

    def reportTareas(self):

        try:

            datos = Conexion.listadoTareasPDF()

            # nombre con fecha
            fecha_hoy = datetime.now().strftime(
                "%Y_%m_%d_%H_%M_%S"
            )

            nombre_pdf = (
                f"informe_tareas_{fecha_hoy}.pdf"
            )

            path = os.path.join(
                self.rootPath,
                nombre_pdf
            )

            pdf = SimpleDocTemplate(path)

            elementos = []

            estilos = styles.getSampleStyleSheet()

            titulo = Paragraph(
                "LISTADO DE TAREAS",
                estilos['Title']
            )

            fecha = Paragraph(

                "Fecha de Impresión: " +

                datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                ),

                estilos['Normal']
            )

            elementos.append(
                titulo
            )

            elementos.append(
                Spacer(1, 20)
            )

            elementos.append(
                fecha
            )

            elementos.append(
                Spacer(1, 20)
            )

            tabla = []

            cabecera = [

                "ID",
                "Cliente",
                "Empleado",
                "Servicio",
                "Horas",
                "Precio",
                "Estado",
                "Total"

            ]

            tabla.append(
                cabecera
            )

            for t in datos:
                total = (
                        float(t[4]) *
                        float(t[5])
                )

                fila = [

                    str(t[0]),
                    str(t[1]),
                    str(t[2]),
                    str(t[3]),
                    str(t[4]),
                    str(t[5]),
                    str(t[6]),
                    f"{total:.2f} €"

                ]

                tabla.append(
                    fila
                )

            tablaPDF = Table(tabla)

            tablaPDF.setStyle([

                ('BACKGROUND',
                 (0, 0),
                 (-1, 0),
                 colors.lightgrey),

                ('TEXTCOLOR',
                 (0, 0),
                 (-1, 0),
                 colors.black),

                ('GRID',
                 (0, 0),
                 (-1, -1),
                 1,
                 colors.black),

                ('ALIGN',
                 (0, 0),
                 (-1, -1),
                 'CENTER'),

                ('FONTNAME',
                 (0, 0),
                 (-1, 0),
                 'Helvetica-Bold'),

                ('BOTTOMPADDING',
                 (0, 0),
                 (-1, 0),
                 12)

            ])

            elementos.append(
                tablaPDF
            )

            pdf.build(
                elementos
            )

            os.startfile(path)

            print(
                "PDF tareas generado"
            )

        except Exception as e:

            print(
                "Error PDF:",
                e
            )