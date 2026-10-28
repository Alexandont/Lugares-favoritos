# Lugares Favoritos

App Android (Kotlin) para la exposición **Firebase, Google Maps API y Seguridad**.
Integra Firebase Authentication, Cloud Firestore, Cloud Storage, Google Maps,
ubicación con FusedLocationProvider y permisos en tiempo de ejecución.

**Flujo:** login → nuevo lugar (nombre + ubicación + foto opcional) → se guarda → aparece en la lista y en el mapa.

## Dónde está cada tema

| Tema | Archivo |
|---|---|
| Authentication | `LoginActivity.kt` |
| Firestore (guardar, consultar, tiempo real) | `NuevoLugarActivity.kt`, `MainActivity.kt`, `MapaActivity.kt` |
| Storage (subir foto y obtener URL) | `NuevoLugarActivity.kt` |
| Permisos de ubicación + ir a Ajustes | `NuevoLugarActivity.kt` y `AndroidManifest.xml` |
| Photo Picker (sin permisos de almacenamiento) | `NuevoLugarActivity.kt` |
| Ubicación (FusedLocationProvider) | `NuevoLugarActivity.kt` |
| Google Maps (marcadores y encuadre) | `MapaActivity.kt` |
| Reglas de seguridad | `firestore.rules`, `storage.rules` |

## Puesta en marcha (en orden)

1. **Archivo de Firebase**: el archivo debe llamarse exactamente `google-services.json`
   (sin espacios ni "(1)") y estar dentro de la carpeta `app/`.
2. **Authentication** → Comenzar → Método de acceso → **Correo electrónico/contraseña** → Habilitar.
3. **Firestore Database** → Crear base de datos (modo producción, región cercana) →
   pestaña **Reglas** → pegar `firestore.rules` → Publicar.
4. **Storage** (para las fotos): desde febrero de 2026 Cloud Storage exige el **plan Blaze**
   (pago por uso, con cuota gratuita). Al pasar a Blaze configura una **alerta de presupuesto**.
   Luego Storage → Comenzar → pestaña **Reglas** → pegar `storage.rules` → Publicar.
   Si no activan Storage, la app igual funciona: guarda el lugar sin foto y avisa.
5. **Google Maps**: en Google Cloud Console (mismo proyecto) habilitar **Maps SDK for Android**,
   crear una API key y pegarla en `secrets.properties`: `MAPS_API_KEY=tu_clave`.
   Maps también necesita una cuenta de facturación vinculada (la misma del plan Blaze sirve).
6. En Android Studio: **File → Sync Project with Gradle Files**, luego
   **Build → Clean Project** y **Build → Rebuild Project**.
7. **Desinstala** la app del emulador/celular y vuelve a ejecutarla.
8. Usa un emulador con **Google Play** (imagen "Google Play" o "Google APIs").
   Para la ubicación: Extended controls (⋯) → Location → fija un punto → Set location.

## Errores comunes

| Mensaje | Causa | Solución |
|---|---|---|
| `API key not valid` | La app se compiló con otro `google-services.json` o con el archivo mal nombrado | Paso 1 + Clean/Rebuild + desinstalar. Si persiste, vuelve a descargar el JSON desde Configuración del proyecto |
| `CONFIGURATION_NOT_FOUND` / `OPERATION_NOT_ALLOWED` | Authentication no habilitado | Paso 2 |
| `The database (default) does not exist` | Firestore no creado | Paso 3 |
| `PERMISSION_DENIED` en Firestore | Reglas no publicadas o usuario sin sesión | Publicar `firestore.rules` |
| Mapa gris sin calles | Falta la API key de Maps o la facturación | Paso 5 |
| "No se pudo subir la foto" | Storage no activado (requiere Blaze) | Paso 4 |

`secrets.properties` y `google-services.json` están en `.gitignore`: no los subas a repositorios públicos.
