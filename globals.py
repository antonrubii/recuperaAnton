"""
Módulo de Variables Globales del Proyecto.

Almacena referencias cruzadas globales que necesitan compartirse dinámicamente entre
módulos aislados, principalmente la instancia activa de la UI para evitar dependencias circulares.
"""
ui = None
"""
Instancia compartida de la interfaz de usuario (Ui_MainWindow). 
Permite acceder a los widgets de la ventana desde cualquier clase externa de lógica.
"""
idCliValido = None  #  ID del cliente seleccionado
idEmpValido = None  #  ID del empleado seleccionado