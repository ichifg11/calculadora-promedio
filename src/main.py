
import flet as ft
import logic


def main(page:ft.Page):
    logic.inicializar(page)
    page.title = "Calcular Promedio"
    page.theme = ft.Theme(color_scheme_seed="indigo")
    page.theme_mode = "system"
    page.scroll = "adaptive"
    page.padding = 20

    #---------------------------
    #---       UI Helpers    ---
    #---------------------------

    def crear_tarjeta_dato(titulo, control_valor, icono, color_icono, color_fondo):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icono, color=color_icono, size=24),
                ft.Text(titulo, size=11, color="grey", weight="w500"),
                control_valor 
            ], 
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            height=90,
            bgcolor=color_fondo,
            border_radius=15,
            padding=10,
            shadow=ft.BoxShadow(
                blur_radius=5,
                color=ft.Colors.with_opacity(0.1, "black"),
                offset=ft.Offset(0, 2)
            )
        )
    #--------------------------------------------------
    #--- REGISTRO ESTUDIANTE / MATERIA / EVALUACION ---
    #--------------------------------------------------

    datos = logic.cargar_datos_estudiantes()

    #Estudiante Variables
    nombre_input = ft.TextField(label="Nombre")
    apellido_input = ft.TextField(label="Apellido")
    carrera_input = ft.TextField(label="Carrera")
    semestre_input = ft.TextField(label="Semestre")


    #Materias

    dd_estudiantes_dashboard = ft.Dropdown(label="Seleccionar Estudiante", width=400)
    dd_estudiantes_materia = ft.Dropdown(label="Seleccionar Estudiante", width=400)
    nombre_materia_input = ft.TextField(label="Nombre de la Materia")
    creditos_input = ft.TextField(label="Créditos", keyboard_type="number")
 

    est_activo = logic.buscar_estudiante_por_nombre(datos, dd_estudiantes_dashboard.value)

    #Evaluaciones
    evaluacion_input = ft.TextField(label="Evaluación")
    dd_materias = ft.Dropdown(label="Seleccionar Materia")
    porcentaje_input = ft.TextField(label="Porcentaje", keyboard_type="number")
    nota_input = ft.TextField(label="Nota", keyboard_type="number")
    base_input = ft.TextField(label="Base de la nota", keyboard_type="number")



    def actualizar_dropdown_estudiantes():
        dd_estudiantes_dashboard.options.clear()
        dd_estudiantes_materia.options.clear()
        for estudiante in datos:
            if isinstance(estudiante, dict):
                nombre_completo = f"{estudiante.get('nombre','')} {estudiante.get('apellido','')}"
            else:
                nombre_completo = f"{getattr(estudiante, 'nombre', '')} {getattr(estudiante, 'apellido', '')}"
            opt = ft.dropdown.Option(text=nombre_completo)
            dd_estudiantes_dashboard.options.append(opt)
            dd_estudiantes_materia.options.append(ft.dropdown.Option(text=nombre_completo))
        
        page.update()


    def registrar_estudiante(e):
        if not nombre_input.value or not apellido_input.value or not carrera_input.value or not semestre_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, llena los campos obligatorios"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return
        logic.registrar_estudiante(datos, nombre_input.value, apellido_input.value, carrera_input.value, semestre_input.value)
        actualizar_dropdown_estudiantes()
        nombre_input.value = ""
        apellido_input.value = ""
        carrera_input.value = ""
        semestre_input.value = ""

    page.snack_bar = ft.SnackBar(ft.Text("Estudiante guardado"), bgcolor="green")
    page.snack_bar.open = True
    page.update()
    btn_registrar_estudiante = ft.Button("Registrar Estudiante", on_click=registrar_estudiante)


    def actualizar_dropdown_materias():
        dd_materias.options.clear()

        if est_activo and hasattr(est_activo, 'materias'):
            for materia in est_activo.materias:
                mat = f"{materia.materia}"
                dd_materias.options.append(ft.dropdown.Option(text=mat))
        
        page.update()


    #Registar Materia--------
    def registrar_materia(e):
        nonlocal est_activo
        estudiante_sel = dd_estudiantes_materia.value or dd_estudiantes_dashboard.value
        if not estudiante_sel:
            page.snack_bar = ft.SnackBar(ft.Text("Debes seleccionar un estudiante"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return
            
        if not nombre_materia_input.value or not creditos_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Faltan datos"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return
        
        est_activo = logic.buscar_estudiante_por_nombre(datos, estudiante_sel)

        if est_activo:
            logic.registrar_materia(datos, est_activo, nombre_materia_input.value, creditos_input.value)
            page.snack_bar = ft.SnackBar(ft.Text(f"Materia agregada a {est_activo.nombre}"), bgcolor="green")
            page.snack_bar.open = True
            nombre_materia_input.value = ""
            creditos_input.value = ""
            actualizar_dropdown_estudiantes()
            actualizar_dropdown_materias()
            actualizar_interfaz_dashboard()
            page.update()
        else:
            print("Error: No se encontró el estudiante seleccionado")

    btn_guardar_materia = ft.Button("Agregar Materia", on_click=registrar_materia)
    actualizar_dropdown_estudiantes()
    

    #Registrar evaluacion -----
    def registrar_evaluacion(e):
        nonlocal est_activo
        estudiante_sel = dd_estudiantes_materia.value or dd_estudiantes_dashboard.value
        if not estudiante_sel:
            page.snack_bar = ft.SnackBar(ft.Text("Debes seleccionar un estudiante"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        est_activo = logic.buscar_estudiante_por_nombre(datos, estudiante_sel)

        materia_seleccionada = dd_materias.value
        if not materia_seleccionada:
            page.snack_bar = ft.SnackBar(ft.Text("Debes seleccionar una materia"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        if est_activo:
            if not getattr(est_activo, 'materias', None):
                page.snack_bar = ft.SnackBar(ft.Text("El estudiante no tiene materias registradas"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return

            materia_obj = None
            for m in est_activo.materias:
                if getattr(m, 'materia', None) == materia_seleccionada:
                    materia_obj = m
                    break

            if materia_obj is None:
                page.snack_bar = ft.SnackBar(ft.Text("Materia seleccionada no encontrada"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return

            try:
                porcentaje_val = float(porcentaje_input.value)
                nota_val = float(nota_input.value)
                if base_input.value in (None, ""):
                    base_val = 20
                else:
                    base_val = int(base_input.value)
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text("Por favor ingresa porcentaje, nota y base válidos"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return

            try:
                logic.add_evaluacion(datos, materia_obj, evaluacion_input.value, porcentaje_val, nota_val, base_val)

                for i, item in enumerate(datos):
                    nombre_item = item.get('nombre') if isinstance(item, dict) else getattr(item, 'nombre')
                    apellido_item = item.get('apellido') if isinstance(item, dict) else getattr(item, 'apellido')
                    if nombre_item == est_activo.nombre and apellido_item == est_activo.apellido:
                        datos[i] = est_activo 
                        break
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error al agregar evaluación: {ex}"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return

            page.snack_bar = ft.SnackBar(ft.Text(f"Evaluación registrada en {materia_seleccionada}"), bgcolor="green")
            page.snack_bar.open = True
            actualizar_dropdown_materias()
            actualizar_interfaz_dashboard()
            actualizar_promedio_general()
            page.update()
            evaluacion_input.value = ""
            porcentaje_input.value = ""
            nota_input.value = ""
            base_input.value = ""

        else:
            print("Error: No se encontró el estudiante seleccionado")
    btn_guardar_evaluacion = ft.Button("Registrar evaluación", on_click=registrar_evaluacion)
    actualizar_dropdown_materias()
  

    #--------------------------------------------------
    #-------           DASHBOARD           ------------
    #--------------------------------------------------

    # Resumen Estudiante

    txt_nombre_dash = ft.Text("Selecciona Estudiante", size=25, weight="bold")
    txt_valor_promedio = ft.Text("0.0", size=25, weight="bold", color="brown")
    txt_valor_semestre = ft.Text("-", size=25, weight="bold", color="brown")
    txt_valor_carrera = ft.Text("-", size=14, weight="bold", color="brown")
    card_promedio = crear_tarjeta_dato(
        "Promedio", 
        txt_valor_promedio,  
        ft.Icons.ANALYTICS, 
        "brown400", 
        "brown50"
    )

    card_semestre = crear_tarjeta_dato(
        "Semestre", 
        txt_valor_semestre,
        ft.Icons.CALENDAR_MONTH, 
        "brown300", 
        "deepOrange50"
    )

    card_carrera = crear_tarjeta_dato(
        "Carrera", 
        txt_valor_carrera,    
        ft.Icons.SCHOOL, 
        "blueGrey400", 
        "blueGrey50"
    )
    student_header_container = ft.Container(
        content=ft.Column([
            txt_nombre_dash,
            ft.Divider(height=5, color="transparent"),
            ft.ResponsiveRow([
                ft.Column([card_promedio], col={"xs": 12, "md": 4}),
                ft.Column([card_semestre], col={"xs": 6,  "md": 4}),
                ft.Column([card_carrera],  col={"xs": 6,  "md": 4}),
            ])
            
        ]),
        padding=5, 
        border=ft.border.all(1, "grey300"), 
        border_radius=10,
        expand=True,
    )

    
    #Actualizar promedio general
    def actualizar_promedio_general():
        if not est_activo:
            return 0.0
        else:
            if not est_activo.materias:
                return 0.0
            else:
                for m in est_activo.materias:
                    if len(m.evaluaciones) == 1:
                        m.promedio = ((m.evaluaciones[0].nota) * 20) / (m.evaluaciones[0].base)
                    else:
                        m.calcular_promedio()
                est_activo.calcular_promedio()
                return

    #Acciones rápidas ------ dashboard
    def go_to(index, e=None):
        class _C: pass
        class _E: pass
        _E.control = _C()
        _E.control.selected_index = index
        try:
            navegar(_E)
        except Exception:
            try:
                page.navigation_bar.selected_index = index
                page.update()
            except Exception:
                pass
    

    acciones_rapidas = ft.Card(
        content=ft.Container(
            padding=15,
            content=ft.Column([
                ft.Text("Acciones Rápidas", weight="bold"),
                ft.Button("Nueva Materia", icon=ft.Icons.BOOK, on_click=lambda e: go_to(4)),
                ft.Button("Nueva Evaluación", icon=ft.Icons.ADD_CHART, on_click=lambda e: go_to(5)),
                ft.Button("Actualizar promedio", icon=ft.Icons.REFRESH_ROUNDED , on_click=actualizar_promedio_general())
            ])
        )
    )

    #Tabla  promedios ---- dashboard
    contenedor_tabla = ft.Container(
        content=ft.Column(expand=True, scroll="adaptive"), 
        border=ft.border.all(1),
        border_radius=10,
        padding=10,
        bgcolor="surfaceVariant", 
        expand=True
    )
    def actualizar_tabla_promedios():
        
        contenedor_tabla.content.controls.clear()
        filas = []
        if est_activo and est_activo.materias:
            for materia in est_activo.materias:
                prom = materia.calcular_promedio()
                m_nombre = materia.materia
                filas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(materia.materia)),
                            ft.DataCell(ft.Text(f"{prom:.2f}")),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE, 
                                    icon_color="red",
                                    tooltip="Eliminar Materia",
                                    data=(est_activo, m_nombre), 
                                    on_click=click_eliminar_materia
                                )
                            )
                        ]
                    )
                )

            tabla_promedios = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Materia")),
                    ft.DataColumn(ft.Text("Promedio")),
                    ft.DataColumn(ft.Text("    "))
                ], rows=filas
            )
            contenedor_tabla.content.controls.append(tabla_promedios)
        else:
            contenedor_tabla.content.controls.append(ft.Text("No hay materias registradas."))
        
        page.update()


    # Interfaz --- dashboard
    def actualizar_interfaz_dashboard():
        if est_activo:
            txt_nombre_dash.value = f"{est_activo.nombre} {est_activo.apellido}"
            card_carrera.value = est_activo.carrera
            card_semestre.value = f"Semestre: {est_activo.semestre}"
            prom_global = est_activo.calcular_promedio()
            card_promedio.value = f"{prom_global:.2f}"

            actualizar_tabla_promedios() 
            actualizar_promedio_general()
        
        page.update()

    def cambio_estudiante(e):
        nonlocal est_activo
        selected_name = dd_estudiantes_dashboard.value or dd_estudiantes_materia.value
        if not selected_name:
            try:
                selected_name = getattr(e.control, 'value', None)
            except Exception:
                selected_name = None

        if not selected_name:
            try:
                idx = getattr(e.control, 'selected_index', None)
                if idx is not None and idx >= 0:
                    opt = e.control.options[idx]
                    selected_name = getattr(opt, 'text', None)
            except Exception:
                selected_name = None

        if not selected_name:
            return
        est_activo = logic.buscar_estudiante_por_nombre(datos, selected_name)
        try:
            dd_estudiantes_dashboard.value = selected_name
            dd_estudiantes_materia.value = selected_name
        except Exception as ex:
            print("cambio_estudiante: could not set dropdown values:", ex)
        
        if est_activo:
            try:
                prom = est_activo.calcular_promedio() 
                txt_valor_promedio.value = f"{prom:.2f}"
            except:
                txt_valor_promedio.value = "0.0"

            txt_valor_semestre.value = str(est_activo.semestre)
            txt_valor_carrera.value = str(est_activo.carrera)
        else:
            txt_valor_promedio.value = "0.0"
            txt_valor_semestre.value = "-"
            txt_valor_carrera.value = "-"

        actualizar_interfaz_dashboard()
        actualizar_tabla_promedios()
        actualizar_dropdown_materias()
        actualizar_promedio_general()
        page.update()


    dd_estudiantes_dashboard.on_change = cambio_estudiante
    dd_estudiantes_materia.on_change = cambio_estudiante


    #Actualizar todo
    def refrescar_todo_el_perfil():
        est_activo = logic.buscar_estudiante_por_nombre(datos, dd_estudiantes_dashboard.value)
        
        if est_activo:
            try:
                prom_gen = est_activo.calcular_promedio() 
                txt_valor_promedio.value = f"{prom_gen:.2f}"
                

                txt_valor_semestre.value = str(est_activo.semestre)
                txt_valor_carrera.value = str(est_activo.carrera)
            except Exception as e:
                txt_valor_promedio.value = "0.0"
                print(f"Error calculando promedio: {e}")

            actualizar_tabla_promedios() 
            actualizar_tabla_evaluaciones() 
            actualizar_promedio_general()
            
        else:
            txt_valor_promedio.value = "0.0"
            contenedor_tabla.content = ft.Text("Selecciona un estudiante")
            contenedor_tabla_evaluaciones.content = ft.Text("Selecciona un estudiante")

        page.update()

    #----------------------------------------
    #---   Evaluaciones estudiante activo ---
    #----------------------------------------

    #Tabla evaluaciones
    contenedor_tabla_evaluaciones = ft.Container(
        content=ft.Column(expand=True, scroll="adaptive"), 
        border=ft.border.all(1),
        border_radius=10,
        padding=10,
        bgcolor="surfaceVariant",
        expand=True
    )
    def actualizar_tabla_evaluaciones():
        contenedor_tabla_evaluaciones.content = None
        
        filas = []
        if est_activo and hasattr(est_activo, 'materias'):
            for materia in est_activo.materias:
                m_nombre = getattr(materia, 'materia', '') or materia.get('materia', 'Sin nombre')
                evals = getattr(materia, 'evaluaciones', [])

                for ev in evals:
                    ev_nombre = getattr(ev, 'evaluacion', '') or getattr(ev, 'nombre', '')
                    nota = getattr(ev, 'nota', 0)
                    base = getattr(ev, 'base', 20)
                    porc = getattr(ev, 'porcentaje', 0)

                    filas.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(m_nombre))),
                                ft.DataCell(ft.Text(str(ev_nombre))),
                                ft.DataCell(ft.Text(f"{nota} / {base}")),
                                ft.DataCell(ft.Text(f"{porc}%")),
                                ft.DataCell(
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_FOREVER,
                                        icon_color="red",
                                        tooltip="Eliminar evaluación",
                                        data=(est_activo, m_nombre, ev_nombre),
                                        on_click=click_eliminar_evaluacion
                                    )
                                )
                            ]
                        )
                    )

        if filas:
            tabla = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Materia", weight="bold")),
                    ft.DataColumn(ft.Text("Evaluación", weight="bold")),
                    ft.DataColumn(ft.Text("Nota", weight="bold")),
                    ft.DataColumn(ft.Text("Porcentaje", weight="bold")),
                    ft.DataColumn(ft.Text(".  ", weight="bold")),
                ],
                rows=filas
            )
            contenedor_tabla_evaluaciones.content = ft.Column([tabla], scroll="adaptive")
        
        else:
            contenedor_tabla_evaluaciones.content = ft.Text("No hay evaluaciones registradas.", italic=True, color="grey")

        page.update()
        


    #----------------------------------------
    #-------   Estudiantes generales  -------
    #----------------------------------------

    contenedor_tabla_estudiantes = ft.Container(
        content=ft.Column(expand=True, scroll="adaptive"), 
        border=ft.border.all(1),
        border_radius=10,
        padding=10,
        bgcolor="surfaceVariant", 
        expand=True
    )

    def actualizar_tabla_estudiantes():
        contenedor_tabla_estudiantes.content.controls.clear()
        filas = []
        
        if datos:
            for estudiante in datos:
                nombre = ""
                carrera = ""
                semestre = ""
                prom = 0.0

                if isinstance(estudiante, dict):
                    nombre = f"{estudiante.get('nombre','')} {estudiante.get('apellido','')}"
                    carrera = estudiante.get('carrera','')
                    semestre = estudiante.get('semestre', '')
                    
                    materias = estudiante.get('materias', [])
                    suma_promedios_materia = 0
                    suma_creditos = 0

                    for m in materias:
                        creditos = float(m.get('creditos', 0) or 0)
                        evaluaciones = m.get('evaluaciones', [])
                        
                        acumulado_materia = 0
                        for ev in evaluaciones:
                            nota = float(ev.get('nota', 0) or 0)
                            base = float(ev.get('base', 20) or 20)
                            porcentaje = float(ev.get('porcentaje', 0) or 0)
                            
                            puntos_obtenidos = (nota / base) * porcentaje
                            acumulado_materia += puntos_obtenidos
                    
                        nota_materia_escala_20 = (acumulado_materia * 20) / 100
                        
                        suma_promedios_materia += nota_materia_escala_20 * creditos
                        suma_creditos += creditos

                    if suma_creditos > 0:
                        prom = suma_promedios_materia / suma_creditos
                    else:
                        prom = 0.0
                else:
                    nombre = f"{getattr(estudiante,'nombre','')} {getattr(estudiante,'apellido','')}"
                    carrera = getattr(estudiante, 'carrera', '')
                    semestre = getattr(estudiante, 'semestre', '')
                    try:
                        prom = float(estudiante.calcular_promedio())
                    except Exception:
                        prom = 0.0

                filas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(nombre)),
                            ft.DataCell(ft.Text(carrera)),
                            ft.DataCell(ft.Text(str(semestre))),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(f"{prom:.2f}", color="white", weight="bold"),
                                    bgcolor="green" if prom >= 9.5 else ("orange" if prom >= 5 else "red"), 
                                    border_radius=10,  
                                    padding=2,   
                                    width=60,         
                                    height=25,
                                   alignment=ft.Alignment(0, 0)
                            )),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.DELETE, 
                                    icon_color="red",
                                    data=estudiante,
                                    on_click=click_eliminar_estudiante
                                )
                            )
                        ]
                    )
                )

            tabla_estudiantes = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Estudiante")),
                    ft.DataColumn(ft.Text("Carrera")),
                    ft.DataColumn(ft.Text("Semestre")),
                    ft.DataColumn(ft.Text("Promedio")),
                    ft.DataColumn(ft.Text("    "))
                ], rows=filas
            )
            contenedor_tabla_estudiantes.content.controls.append(tabla_estudiantes)
        else:
            contenedor_tabla_estudiantes.content.controls.append(ft.Text("No hay estudiantes registrados."))

        page.update()

               

    #-------------------------
    #---  Delete  Buttons  ---
    #-------------------------
    def click_eliminar_estudiante(e):
        est_a_borrar = e.control.data
        if logic.eliminar_estudiante(datos, est_a_borrar):
            page.snack_bar = ft.SnackBar(ft.Text(f"Estudiante eliminado"), bgcolor="red")
            page.snack_bar.open = True
            nonlocal est_activo
            if est_activo == est_a_borrar:
                est_activo = None
                txt_valor_promedio.value = "0.0"
                txt_valor_semestre.value = "-"
                txt_valor_carrera.value = "-"
            
            actualizar_tabla_estudiantes()
            actualizar_dropdown_estudiantes() 
            page.update()
        refrescar_todo_el_perfil()

    def click_eliminar_materia(e):
        est_obj, nombre_mat = e.control.data 
        if logic.eliminar_materia(datos, est_obj, nombre_mat):
            page.snack_bar = ft.SnackBar(ft.Text(f"Materia '{nombre_mat}' eliminada"), bgcolor="red")
            page.snack_bar.open = True
            actualizar_interfaz_dashboard() 
        page.update()
        refrescar_todo_el_perfil()

    def click_eliminar_evaluacion(e):
        est_obj, nom_mat, nom_ev = e.control.data
        if logic.eliminar_evaluacion(datos, est_obj, nom_mat, nom_ev):
            page.snack_bar = ft.SnackBar(ft.Text("Evaluación eliminada"), bgcolor="red")
            page.snack_bar.open = True
            actualizar_tabla_evaluaciones()
            actualizar_interfaz_dashboard()
        page.update()
        refrescar_todo_el_perfil()


    #--------------------------------
    #----       NAVEGACIÓN       ----
    #--------------------------------

    #TAB Dashboard
    btn_probar_seleccion = ft.Button("Seleccionar", on_click=cambio_estudiante)
    tab_dashboard = ft.ListView([ 
        ft.Row([dd_estudiantes_dashboard, btn_probar_seleccion]),
        student_header_container,
        
        ft.Divider(height=20, color="transparent"),
        ft.ResponsiveRow([
            ft.Column([contenedor_tabla], col={"xs": 12, "md": 8}),
            ft.Column([acciones_rapidas], col={"xs": 12, "md": 4}), 
        ], vertical_alignment=ft.CrossAxisAlignment.START)
        
    ], visible=True, spacing=10, padding=10)

    #TAB Evaluaciones estudiante
    tab_evaluaciones_est = ft.Column([
        ft.Text(f"Evaluaciones: {est_activo}", size=20, weight="bold"),
        contenedor_tabla_evaluaciones
    ], visible=False)

    #TAB Estudiantes
    tab_lista_estudiantes = ft.Column([
        ft.Text("Listado General", size=20, weight="bold"),
        contenedor_tabla_estudiantes
    ], visible=False)

    #TAB registro estudiante
    tab_registro_est = ft.Column([
        ft.Text("Registrar Nuevo Estudiante", size=20),
        nombre_input, apellido_input, carrera_input, semestre_input,
        btn_registrar_estudiante
    ], visible=False)

    #TAB registro materia
    tab_registro_materia = ft.Column([
        ft.Text("Registrar Nueva Materia", size=20),
        dd_estudiantes_materia, nombre_materia_input, creditos_input,
        btn_guardar_materia
    ], visible=False)

    #TAB registro evaluacion
    tab_registro_evaluacion = ft.Column([
        ft.Text("Registrar Nueva Evaluación", size=20),
        dd_materias, evaluacion_input, porcentaje_input, nota_input, base_input,
        btn_guardar_evaluacion
    ], visible=False)

    vista_dashboard = tab_dashboard
    vista_ev_estudiante = tab_evaluaciones_est
    vista_lista_estudiantes = ft.Column([
            ft.Text("Listado General de Estudiantes", size=25, weight="bold"),
            contenedor_tabla_estudiantes
        ], visible=False)        
    vista_registro_est = tab_registro_est
    vista_registro_materia = tab_registro_materia
    vista_registro_evaluacion = tab_registro_evaluacion

    def navegar(e):
        index = e.control.selected_index
        vistas = [vista_dashboard, vista_ev_estudiante, vista_lista_estudiantes, vista_registro_est, vista_registro_materia, vista_registro_evaluacion] 
        
        for i, v in enumerate(vistas):
            v.visible = (i == index)
            v.update()
        
        match index:
            case 0:
                actualizar_interfaz_dashboard() 
            case 1:
                tab_evaluaciones_est.update()
                actualizar_tabla_evaluaciones()
            case 2:
                tab_lista_estudiantes,
                actualizar_tabla_estudiantes()
            case 3:
                vista_registro_est.update()
            case 4:
                vista_registro_materia.update()
            case 5:
                vista_registro_evaluacion.update()
                actualizar_dropdown_estudiantes()
            case _:
                raise ValueError("Índice de navegación no reconocido")
        
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.DASHBOARD, label="Dashboard"),
            ft.NavigationBarDestination(icon=ft.Icons.FACT_CHECK, label="Evaluaciones"),
            ft.NavigationBarDestination(icon=ft.Icons.PEOPLE, label="Estudiantes"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_ADD, label="Nuevo Estudiante"),
            ft.NavigationBarDestination(icon=ft.Icons.BOOK, label="Registrar Materia"),
            ft.NavigationBarDestination(icon=ft.Icons.ASSIGNMENT, label="Registrar Evaluación"),
        ],
        on_change=navegar
    )

    page.add(
        vista_dashboard,
        vista_ev_estudiante,
        vista_lista_estudiantes,
        vista_registro_est,
        vista_registro_materia,
        vista_registro_evaluacion
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)