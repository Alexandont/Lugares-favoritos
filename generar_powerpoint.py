import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck(filename="LugaresFavoritos_Exposicion.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette (Dark Theme / Widescreen)
    C_BG = RGBColor(11, 15, 25)           # Fondo principal
    C_CARD_BG = RGBColor(21, 29, 48)      # Tarjetas
    C_CARD_BORDER = RGBColor(35, 49, 82)  # Bordes
    C_WHITE = RGBColor(255, 255, 255)
    C_LIGHT_GRAY = RGBColor(203, 213, 225)
    C_MUTED = RGBColor(148, 163, 184)
    C_SKY = RGBColor(56, 189, 248)         # Acento azul (Android / Maps)
    C_AMBER = RGBColor(245, 158, 11)       # Acento naranja (Firebase)
    C_GREEN = RGBColor(16, 185, 129)       # Acento verde (Geolocalización / Éxito)
    C_CODE_BG = RGBColor(7, 10, 19)

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.color.rgb = C_BG
        return bg

    def add_header(slide, tag_text, title_text):
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(8), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_SKY
        p_tag.font.name = "Arial"

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(25)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE
        p_title.font.name = "Arial"

    def add_card(slide, left, top, width, height, title, items, subtitle=None, code_snippet=None, accent_color=C_SKY):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_CARD_BORDER
        card.line.width = Pt(1.2)

        content_left = left + Inches(0.3)
        content_top = top + Inches(0.25)
        content_width = width - Inches(0.6)

        # Title
        title_box = slide.shapes.add_textbox(content_left, content_top, content_width, Inches(0.4))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = accent_color
        p.font.name = "Arial"

        current_y = content_top + Inches(0.42)

        # Optional Subtitle / Concept definition
        if subtitle:
            sub_box = slide.shapes.add_textbox(content_left, current_y, content_width, Inches(0.4))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.size = Pt(12)
            p_sub.font.italic = True
            p_sub.font.color.rgb = C_MUTED
            p_sub.font.name = "Arial"
            current_y += Inches(0.4)

        # Bullet Items
        if items:
            items_height = Inches(len(items) * 0.42)
            items_box = slide.shapes.add_textbox(content_left, current_y, content_width, items_height)
            tf_items = items_box.text_frame
            tf_items.word_wrap = True
            tf_items.margin_left = tf_items.margin_top = tf_items.margin_right = tf_items.margin_bottom = 0

            for i, itm in enumerate(items):
                p_item = tf_items.paragraphs[0] if i == 0 else tf_items.add_paragraph()
                p_item.text = f"• {itm}"
                p_item.font.size = Pt(12)
                p_item.font.color.rgb = C_LIGHT_GRAY
                p_item.font.name = "Arial"
                p_item.space_after = Pt(6)
            current_y += items_height

        # Optional Code Snippet Box
        if code_snippet:
            code_top = current_y + Inches(0.08)
            code_height = height - (code_top - top) - Inches(0.2)
            if code_height > Inches(0.8):
                code_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, content_left, code_top, content_width, code_height)
                code_bg.fill.solid()
                code_bg.fill.fore_color.rgb = C_CODE_BG
                code_bg.line.color.rgb = C_CARD_BORDER
                code_bg.line.width = Pt(0.8)

                code_box = slide.shapes.add_textbox(content_left + Inches(0.18), code_top + Inches(0.12), content_width - Inches(0.36), code_height - Inches(0.24))
                tf_code = code_box.text_frame
                tf_code.word_wrap = True
                tf_code.margin_left = tf_code.margin_top = tf_code.margin_right = tf_code.margin_bottom = 0
                for line_idx, line in enumerate(code_snippet.split("\n")):
                    p_line = tf_code.paragraphs[0] if line_idx == 0 else tf_code.add_paragraph()
                    p_line.text = line
                    p_line.font.size = Pt(9.5)
                    p_line.font.name = "Courier New"
                    p_line.font.color.rgb = RGBColor(226, 232, 240)

    # ==================== SLIDE 1: PORTADA ====================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    hero = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.1), Inches(10.933), Inches(5.3))
    hero.fill.solid()
    hero.fill.fore_color.rgb = C_CARD_BG
    hero.line.color.rgb = C_CARD_BORDER
    hero.line.width = Pt(1.5)

    badge = s1.shapes.add_textbox(Inches(1.8), Inches(1.6), Inches(9.5), Inches(0.4))
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "DESARROLLO MÓVIL EN ANDROID CON KOTLIN"
    p_b.font.size = Pt(12)
    p_b.font.bold = True
    p_b.font.color.rgb = C_AMBER
    p_b.font.name = "Arial"

    tbox = s1.shapes.add_textbox(Inches(1.8), Inches(2.1), Inches(9.8), Inches(1.8))
    tf_t = tbox.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "Firebase en Android, Geolocalización y Google Maps"
    p_t.font.size = Pt(34)
    p_t.font.bold = True
    p_t.font.color.rgb = C_WHITE
    p_t.font.name = "Arial"

    desc = s1.shapes.add_textbox(Inches(1.8), Inches(4.2), Inches(9.8), Inches(1.6))
    tf_d = desc.text_frame
    tf_d.word_wrap = True
    p_d = tf_d.paragraphs[0]
    p_d.text = "Fundamentos teóricos esenciales y aplicación práctica en proyecto real:\n" \
               "• Backend as a Service (BaaS) con Firebase Authentication, Cloud Firestore y Cloud Storage\n" \
               "• Modelo de Permisos en Android (Runtime Permissions y Rationale)\n" \
               "• Geolocalización con FusedLocationProviderClient y visualización con Google Maps SDK\n" \
               "• Caso de Estudio en Kotlin: App 'Lugares Favoritos'"
    p_d.font.size = Pt(13.5)
    p_d.font.color.rgb = C_LIGHT_GRAY
    p_d.font.name = "Arial"

    # ==================== SLIDE 2: TEORÍA: ¿QUÉ ES FIREBASE Y BAAS? ====================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Fundamentos Teóricos", "¿Qué es Firebase y la Arquitectura BaaS?")

    add_card(s2, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Concepto: Backend as a Service (BaaS)", [
                 "Definición: Paradigma donde el proveedor en la nube suministra y administra la infraestructura de backend (servidores, bases de datos, autenticación, storage, balanceo de carga).",
                 "Enfoque Client-Centric: Los desarrolladores móviles interactúan directamente mediante SDKs nativos sin necesidad de programar ni mantener APIs REST intermedias.",
                 "Escalabilidad Elástica: El aprovisionamiento de recursos y la alta disponibilidad son gestionados automáticamente por los centros de datos de Google.",
                 "Reducción de Time-to-Market: Se elimina el 70% del código repetitivo de backend (CRUDs básicos, sockets y gestión de tokens)."
             ], subtitle="Evolución de la arquitectura cliente-servidor tradicional", accent_color=C_AMBER)

    add_card(s2, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1),
             "Comparativa de Modelos Arquitectónicos", [
                 "Backend Tradicional (Spring / Node / Django):\n- Requiere hosting dedicado, configuración de proxies inversos y certificados SSL.\n- Obliga a crear endpoints HTTP, serialización manual y mantenimiento de base de datos relacional.",
                 "Ecosistema Firebase en Android:\n- SDK oficial integrado mediante Gradle con el Firebase BoM.\n- Protocolos binarios de alto rendimiento (gRPC y HTTP/2).\n- Sincronización offline automática con SQLite local.\n- Reglas de seguridad basadas en el servidor."
             ], subtitle="¿Por qué la industria adopta BaaS para aplicaciones móviles?", accent_color=C_SKY)

    # ==================== SLIDE 3: TEORÍA: FIREBASE AUTHENTICATION ====================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Fundamentos Teóricos", "Firebase Authentication: Identidad y Seguridad")

    add_card(s3, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "¿Qué es y qué problema resuelve?", [
                 "Definición: Servicio integral de identidad que abstrae la gestión segura de cuentas, contraseñas y proveedores federados (Google, Apple, Facebook).",
                 "Criptografía en Servidor: Las contraseñas nunca se guardan en texto plano; se encriptan con algoritmos robustos (scrypt/bcrypt) inmunes a ataques de diccionario.",
                 "Tokens JWT (JSON Web Tokens): Tras verificar credenciales, emite un par de tokens criptográficos: ID Token (validez corta) y Refresh Token (para renovar sesión de fondo).",
                 "Integración con el Ecosistema: El UID generado identifica al usuario de forma única en Cloud Firestore y Cloud Storage."
             ], subtitle="Manejo moderno de identidad y control de acceso", accent_color=C_AMBER)

    add_card(s3, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1),
             "Persistencia de Sesión y Ciclo de Vida", [
                 "Almacenamiento Local Seguro: El SDK de Firebase guarda las credenciales cifradas en el dispositivo móvil sin que el programador deba recurrir a SharedPreferences.",
                 "Auto-Login Transparente: Al abrir la aplicación, el SDK evalúa de inmediato si existe una sesión válida activa (auth.currentUser != null).",
                 "Llamadas Asíncronas No Bloqueantes: Cada petición corre en hilos secundarios y devuelve una Task<AuthResult>, evitando que la interfaz sufra congelamientos (ANR)."
             ], subtitle="Cómo funciona la sesión bajo el capó", accent_color=C_SKY)

    # ==================== SLIDE 4: PRÁCTICA: AUTHENTICATION EN ANDROID ====================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Implementación Práctica", "Authentication en LoginActivity.kt")

    add_card(s4, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Lógica de Verificación y Flujo", [
                 "Comprobación en onCreate(): Si ya existe sesión previa, salta inmediatamente el formulario con irAlInicio().",
                 "Validación defensiva: Se comprueba formato de correo y que la contraseña cumpla el mínimo de 6 caracteres exigido por Firebase.",
                 "signInWithEmailAndPassword(): Inicia sesión con usuario existente.",
                 "createUserWithEmailAndPassword(): Registra nuevo usuario y genera automáticamente su UID único."
             ], subtitle="Patrón de inicio rápido y control de errores en cliente", accent_color=C_AMBER)

    add_card(s4, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1),
             "Código Fuente: LoginActivity.kt", [
                 "Uso de Tasks asíncronas con callbacks al hilo principal:"
             ], code_snippet="// LoginActivity.kt\noverride fun onCreate(savedInstanceState: Bundle?) {\n    super.onCreate(savedInstanceState)\n    // Si la sesión ya existe en el dispositivo, se salta el login\n    if (auth.currentUser != null) {\n        irAlInicio()\n        return\n    }\n    \n    b.btnIngresar.setOnClickListener {\n        val (email, pass) = leerDatos() ?: return@setOnClickListener\n        auth.signInWithEmailAndPassword(email, pass)\n            .addOnCompleteListener { t ->\n                resultado(t.isSuccessful, t.exception?.localizedMessage)\n            }\n    }\n}", accent_color=C_SKY)

    # ==================== SLIDE 5: TEORÍA: CLOUD FIRESTORE (NOSQL) ====================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Fundamentos Teóricos", "Cloud Firestore: Base de Datos NoSQL y Tiempo Real")

    add_card(s5, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "¿Qué es una Base de Datos NoSQL Documental?", [
                 "Modelo Orientado a Documentos: A diferencia de SQL (filas, columnas y tablas con esquemas fijos), Firestore organiza la información en Colecciones y Documentos (formato JSON flexible).",
                 "Estructura Jerárquica: Colección ('lugares') -> Documento ('id_autogenerado') -> Campos ('nombre', 'lat', 'lng', 'uid', 'creado').",
                 "Consultas Indexadas: Cada consulta es rápida sin importar el tamaño total de la base de datos porque Firestore indexa todos los campos por defecto.",
                 "Persistencia Offline: Almacena una copia SQLite local en el teléfono que permite leer y escribir aun cuando no hay internet."
             ], subtitle="Diferencias clave frente al modelo relacional tradicional", accent_color=C_AMBER)

    add_card(s5, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1),
             "Sincronización en Tiempo Real (Push vs Pull)", [
                 "Modelo Tradicional (Pull / Polling): El cliente hace peticiones HTTP GET periódicas al servidor para ver si hay cambios (ineficiente, satura red y batería).",
                 "Modelo Firestore (Push / Snapshot): Establece una conexión persistente bidireccional (gRPC sobre HTTP/2). Cuando los datos cambian en la nube, el servidor empuja el nuevo snapshot al cliente de forma instantánea.",
                 "Event-Driven UI: Las vistas de la app se redibujan de forma reactiva sin que el usuario tenga que deslizar para recargar."
             ], subtitle="La magia de los Snapshot Listeners", accent_color=C_GREEN)

    # ==================== SLIDE 6: PRÁCTICA: FIRESTORE EN ANDROID ====================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Implementación Práctica", "Firestore: Modelado y addSnapshotListener")

    add_card(s6, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Modelado Tipado: Lugar.kt", [
                 "Data Class de Kotlin con propiedades fuertemente tipadas.",
                 "Valores por defecto: Indispensables para que Firestore pueda instanciar los objetos por reflexión mediante toObjects(Lugar::class.java).",
                 "Campos geoespaciales: Latitud y longitud se guardan como Double para facilitar la posterior proyección en Google Maps."
             ], code_snippet="// Lugar.kt\ndata class Lugar(\n    val nombre: String = \"\",\n    val lat: Double = 0.0,\n    val lng: Double = 0.0,\n    val fotoUrl: String = \"\",\n    val uid: String = \"\",\n    val creado: Long = 0L\n)", accent_color=C_AMBER)

    add_card(s6, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1),
             "Escucha Reactiva en MainActivity.kt", [
                 "Filtro compuesto con whereEqualTo('uid', uid) para aislar datos.",
                 "Actualización automática de la lista en el RecyclerView:"
             ], code_snippet="// MainActivity.kt\noverride fun onStart() {\n    super.onStart()\n    val uid = Firebase.auth.currentUser?.uid ?: return\n    registro = Firebase.firestore.collection(\"lugares\")\n        .whereEqualTo(\"uid\", uid)\n        .addSnapshotListener { snapshot, error ->\n            if (error != null) return@addSnapshotListener\n            val lista = snapshot?.toObjects(Lugar::class.java).orEmpty()\n            adapter.submit(lista.sortedByDescending { it.creado })\n        }\n}", accent_color=C_SKY)

    # ==================== SLIDE 7: TEORÍA: CLOUD STORAGE ====================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Fundamentos Teóricos", "Cloud Storage: Almacenamiento de Objetos Binarios")

    add_card(s7, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "¿Qué es y por qué desacoplar binarios?", [
                 "Definición: Servicio de almacenamiento masivo de objetos no estructurados (fotos, videos, audios) construido sobre Google Cloud Storage.",
                 "Límite de Bases de Datos: Cloud Firestore tiene un límite estricto de 1 MB por documento. Guardar una foto de 4 MB en Base64 saturaría el documento y encarecería la facturación.",
                 "Arquitectura de Referencias: El archivo físico binario se guarda en Storage en un 'bucket', y en Firestore únicamente se almacena la URL de descarga (un string liviano).",
                 "Estructura por Carpetas: Permite organizar archivos jerárquicamente por usuario: fotos/{uid}/{UUID}.jpg."
             ], subtitle="Almacenamiento transaccional vs Almacenamiento de objetos", accent_color=C_AMBER)

    add_card(s7, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1),
             "Pipeline Asíncrono de Subida", [
                 "Paso 1: Subir el archivo local mediante putFile(uri) -> Tarea asíncrona de subida.",
                 "Paso 2: Obtener la URL pública de descarga con ref.downloadUrl -> Segunda tarea asíncrona.",
                 "Paso 3: Guardar el documento en Firestore con la URL resultante.",
                 "Encadenamiento de Tareas: Para evitar anidar múltiples callbacks (Callback Hell), el SDK de Google Tasks provee continueWithTask."
             ], subtitle="Orquestación secuencial de operaciones asíncronas", accent_color=C_SKY)

    # ==================== SLIDE 8: PRÁCTICA: STORAGE EN ANDROID ====================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Implementación Práctica", "Cloud Storage en NuevoLugarActivity.kt")

    add_card(s8, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Pipeline Completo: Subida + Firestore", [
                 "Generación de nombre único con UUID.randomUUID() para evitar colisiones de archivos.",
                 "Partición de carpetas por UID para aplicar reglas de acceso por usuario.",
                 "continueWithTask: Si la subida falla, interrumpe el flujo; si tiene éxito, solicita la URL de descarga."
             ], code_snippet="// NuevoLugarActivity.kt\nval ref = Firebase.storage.reference.child(\"fotos/$uid/${UUID.randomUUID()}.jpg\")\n\nref.putFile(foto)\n    .continueWithTask { t ->\n        if (!t.isSuccessful) throw t.exception!!\n        ref.downloadUrl\n    }\n    .addOnSuccessListener { url ->\n        val lugar = Lugar(nombre, lat, lng, url.toString(), uid, creado)\n        Firebase.firestore.collection(\"lugares\").add(lugar)\n            .addOnSuccessListener { finish() }\n    }", accent_color=C_AMBER)

    add_card(s8, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1),
             "Descarga Optimizada con Coil", [
                 "Librería moderna en Kotlin para carga de imágenes asíncronas.",
                 "Gestión automática de memoria RAM y caché en disco.",
                 "Evita que la aplicación colapse por falta de memoria (OutOfMemoryError) al hacer scroll en la lista."
             ], code_snippet="// LugaresAdapter.kt\noverride fun onBindViewHolder(holder: VH, position: Int) {\n    val lugar = items[position]\n    holder.b.tvNombre.text = lugar.nombre\n    holder.b.tvCoords.text = String.format(\"%.5f, %.5f\", lugar.lat, lugar.lng)\n    // Coil descarga, cachea y renderiza en ImageView\n    holder.b.ivFoto.load(lugar.fotoUrl)\n}", accent_color=C_SKY)

    # ==================== SLIDE 9: TEORÍA: GESTIÓN DE PERMISOS EN ANDROID ====================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Fundamentos Teóricos", "Sistema de Permisos en Android Moderno")

    add_card(s9, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Evolución del Modelo de Permisos", [
                 "Permisos de Instalación (Android 1.0 - 5.1): Se aceptaban todos los permisos al descargar la app. El usuario no tenía control granular.",
                 "Runtime Permissions (Android 6.0+ / API 23): Los permisos peligrosos (Ubicación, Cámara, Micrófono) deben solicitarse en tiempo de ejecución solo cuando se necesitan.",
                 "Ubicación Aproximada vs Precisa (Android 12+ / API 31): El sistema divide la ubicación en ACCESS_COARSE_LOCATION (~3 km) y ACCESS_FINE_LOCATION (~metros). Se deben pedir ambos a la vez.",
                 "Principio de Menor Privilegio: Si una función puede resolverse sin permisos (ej. Photo Picker), esa debe ser la solución prioritaria."
             ], subtitle="Privacidad y control del usuario en el sistema operativo", accent_color=C_GREEN)

    add_card(s9, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1),
             "El Flujo de UX Recomendado por Google", [
                 "Paso 1: checkSelfPermission() -> Verificar si el permiso ya fue concedido.",
                 "Paso 2: shouldShowRequestPermissionRationale() -> Si el usuario ya rechazó la petición previamente, se debe mostrar un diálogo explicativo antes de volver a preguntar.",
                 "Paso 3: Lanzar contrato múltiple del sistema.",
                 "Paso 4: Manejar la respuesta del usuario (aceptada o denegada) sin romper la app."
             ], subtitle="Patrón oficial de experiencia de usuario", accent_color=C_SKY)

    # ==================== SLIDE 10: PRÁCTICA: PERMISOS EN ANDROID ====================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Implementación Práctica", "Permisos y Photo Picker en NuevoLugarActivity.kt")

    add_card(s10, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Photo Picker: Cero Permisos de Disco", [
                 "Uso del contrato moderno ActivityResultContracts.GetContent().",
                 "Ventaja de privacidad: No se declara READ_EXTERNAL_STORAGE ni READ_MEDIA_IMAGES en el manifiesto.",
                 "El sistema abre su propio selector y devuelve un URI temporal seguro de solo lectura."
             ], code_snippet="// NuevoLugarActivity.kt\nprivate val elegirFoto =\n    registerForActivityResult(ActivityResultContracts.GetContent()) { uri ->\n        if (uri != null) {\n            fotoUri = uri\n            b.ivFoto.setImageURI(uri)\n        }\n    }", accent_color=C_GREEN)

    add_card(s10, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1),
             "Flujo con Rationale Dialog", [
                 "Implementación fiel del flujo recomendado de Android:"
             ], code_snippet="// NuevoLugarActivity.kt\nprivate fun solicitarUbicacion() {\n    when {\n        tienePermiso() -> obtenerUbicacion()\n        shouldShowRequestPermissionRationale(Manifest.permission.ACCESS_FINE_LOCATION) ->\n            AlertDialog.Builder(this)\n                .setTitle(R.string.permiso_titulo)\n                .setMessage(R.string.permiso_motivo)\n                .setPositiveButton(R.string.continuar) { _, _ -> lanzarPermisos() }\n                .setNegativeButton(R.string.cancelar, null)\n                .show()\n        else -> lanzarPermisos()\n    }\n}", accent_color=C_SKY)

    # ==================== SLIDE 11: TEORÍA: GEOLOCALIZACIÓN Y GOOGLE MAPS ====================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Fundamentos Teóricos", "Geolocalización Móvil y Google Maps SDK")

    add_card(s11, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "¿Cómo funciona la Geolocalización Móvil?", [
                 "Fuentes de Posicionamiento:\n1. GNSS / GPS Satelital: Muy preciso en exteriores, alto consumo de batería.\n2. Triangulación de Torres Celulares: Rápido, menor precisión (~cuadras).\n3. Escaneo de Redes Wi-Fi: Ubicación en interiores mediante mapeo de MAC addresses.",
                 "FusedLocationProviderClient de Google Play Services:\n- Algoritmo inteligente que fusiona las tres fuentes automáticamente.\n- Optimiza el uso de batería y devuelve coordenadas (lat, lng) precisas.",
                 "Prioridad PRIORITY_HIGH_ACCURACY: Fuerza la lectura más precisa posible para guardar puntos geográficos fijos."
             ], subtitle="Hardware, redes y servicios de ubicación", accent_color=C_GREEN)

    add_card(s11, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1),
             "Google Maps SDK for Android", [
                 "Renderizado Vectorial: Descarga geometrías vectoriales ligeras y las dibuja en GPU (aceleración por hardware).",
                 "SupportMapFragment: Contenedor visual que gestiona el ciclo de vida del mapa (pausa, reanudación, destrucción).",
                 "Proyección de Marcadores: Convierte coordenadas geográficas esféricas (LatLng) en píxeles de pantalla (Marker).",
                 "Cálculo de Bounds: LatLngBounds calcula la caja geográfica mínima que contiene todos los puntos para ajustar la cámara automáticamente."
             ], subtitle="Conceptos cartográficos en dispositivos móviles", accent_color=C_SKY)

    # ==================== SLIDE 12: PRÁCTICA: MAPS Y FUSED LOCATION ====================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Implementación Práctica", "Captura con FusedLocation y Renderizado en Maps")

    add_card(s12, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Captura GPS: NuevoLugarActivity.kt", [
                 "getCurrentLocation(): Garantiza una posición fresca.",
                 "CancellationTokenSource(): Permite cancelar la solicitud si el usuario abandona la pantalla."
             ], code_snippet="// NuevoLugarActivity.kt\n@SuppressLint(\"MissingPermission\")\nprivate fun obtenerUbicacion() {\n    fused.getCurrentLocation(\n        Priority.PRIORITY_HIGH_ACCURACY,\n        CancellationTokenSource().token\n    ).addOnSuccessListener { loc ->\n        if (loc != null) {\n            ubicacion = loc\n            b.tvUbicacion.text = String.format(\"%.5f, %.5f\", loc.latitude, loc.longitude)\n        }\n    }\n}", accent_color=C_GREEN)

    add_card(s12, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1),
             "Encuadre Dinámico: MapaActivity.kt", [
                 "LatLngBounds.Builder agrega todos los puntos.",
                 "setOnMapLoadedCallback: Garantiza que la vista esté dimensionada antes de animar la cámara, evitando crashes."
             ], code_snippet="// MapaActivity.kt\nval bounds = LatLngBounds.Builder()\nlugares.forEach { l ->\n    val pos = LatLng(l.lat, l.lng)\n    map.addMarker(MarkerOptions().position(pos).title(l.nombre))\n    bounds.include(pos)\n}\nif (lugares.size == 1) {\n    map.moveCamera(CameraUpdateFactory.newLatLngZoom(pos, 15f))\n} else {\n    map.setOnMapLoadedCallback {\n        map.moveCamera(CameraUpdateFactory.newLatLngBounds(bounds.build(), 120))\n    }\n}", accent_color=C_SKY)

    # ==================== SLIDE 13: TEORÍA Y PRÁCTICA: REGLAS DE SEGURIDAD ====================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Seguridad en la Nube", "Reglas de Servidor: Firestore y Storage Rules")

    add_card(s13, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Concepto Teórico: Zero-Trust Client", [
                 "El Cliente Nunca es de Confianza: Un usuario malintencionado puede alterar el APK o interceptar peticiones con un proxy HTTP (Charles/Burp).",
                 "Seguridad a Nivel de Servidor: Firebase evalúa cada lectura y escritura mediante un motor de reglas antes de permitir el acceso.",
                 "Multi-tenancy Aislado: Garantiza criptográficamente que cada usuario solo pueda ver, crear o editar sus propios registros comparando request.auth.uid.",
                 "Validación de Integridad: Impide que usuarios anónimos creen datos sin autenticarse."
             ], subtitle="¿Por qué la seguridad móvil se define en el backend?", accent_color=C_AMBER)

    add_card(s13, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1),
             "Reglas en Producción del Proyecto", [
                 "Reglas activas en firestore.rules y storage.rules:"
             ], code_snippet="// firestore.rules\nservice cloud.firestore {\n  match /databases/{db}/documents {\n    match /lugares/{id} {\n      allow read, update, delete: if request.auth != null\n        && resource.data.uid == request.auth.uid;\n      allow create: if request.auth != null\n        && request.resource.data.uid == request.auth.uid;\n    }\n  }\n}\n\n// storage.rules\nmatch /fotos/{uid}/{archivo} {\n  allow read, write: if request.auth != null && request.auth.uid == uid;\n}", accent_color=C_SKY)

    # ==================== SLIDE 14: CONCLUSIONES ====================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Síntesis Final", "Conclusiones y Preguntas")

    add_card(s14, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Resumen Teórico y Práctico", [
                 "1. Arquitectura BaaS: Delegar infraestructura a Firebase acelera el desarrollo y garantiza escalabilidad elástica.",
                 "2. Seguridad Multicapa: Ocultamiento de API Keys (Secrets Plugin) + Reglas de Servidor (request.auth.uid).",
                 "3. Eficiencia en Memoria y Red: Desacoplamiento de binarios en Storage, caché con Coil y cierre de listeners en onStop().",
                 "4. Experiencia de Usuario: Privacidad con Photo Picker, justificación con Rationale y mapas vectoriales fluidos."
             ], subtitle="Lecciones de arquitectura móvil en producción", accent_color=C_GREEN)

    add_card(s14, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1),
             "Espacio para Preguntas", [
                 "¡Muchas gracias por su atención!",
                 "Abierto para consultas teóricas y técnicas sobre el ecosistema Firebase, Android y Google Maps."
             ], code_snippet="// Proyecto de Código Abierto\nLugaresFavoritos (Kotlin + Android SDK 34)\n\n• Firebase Authentication (Email/Password)\n• Cloud Firestore (NoSQL Real-Time)\n• Cloud Storage (Object Storage)\n• Google Play Services Location & Maps SDK", accent_color=C_AMBER)

    prs.save(filename)
    print(f"Presentation successfully updated at: {filename}")

if __name__ == "__main__":
    create_deck()
