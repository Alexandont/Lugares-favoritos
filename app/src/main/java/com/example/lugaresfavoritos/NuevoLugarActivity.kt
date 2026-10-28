package com.example.lugaresfavoritos

import android.Manifest
import android.annotation.SuppressLint
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Location
import android.net.Uri
import android.os.Bundle
import android.provider.Settings
import android.view.View
import android.widget.Toast
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.example.lugaresfavoritos.databinding.ActivityNuevoLugarBinding
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import com.google.android.gms.tasks.CancellationTokenSource
import com.google.firebase.Firebase
import com.google.firebase.auth.auth
import com.google.firebase.firestore.firestore
import com.google.firebase.storage.storage
import java.util.Locale
import java.util.UUID

class NuevoLugarActivity : AppCompatActivity() {

    private lateinit var b: ActivityNuevoLugarBinding
    private var fotoUri: Uri? = null
    private var ubicacion: Location? = null
    private var cancelacion: CancellationTokenSource? = null
    private val fused by lazy { LocationServices.getFusedLocationProviderClient(this) }

    private val elegirFoto =
        registerForActivityResult(ActivityResultContracts.PickVisualMedia()) { uri ->
            if (uri != null) {
                fotoUri = uri
                b.ivFoto.setImageURI(uri)
            }
        }

    private val pedirPermisos =
        registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { r ->
            val fine = r[Manifest.permission.ACCESS_FINE_LOCATION] == true
            val coarse = r[Manifest.permission.ACCESS_COARSE_LOCATION] == true
            when {
                fine || coarse -> obtenerUbicacion()
                !shouldShowRequestPermissionRationale(Manifest.permission.ACCESS_FINE_LOCATION) ->
                    mostrarIrAAjustes()
                else -> Toast.makeText(this, R.string.permiso_denegado, Toast.LENGTH_LONG).show()
            }
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        b = ActivityNuevoLugarBinding.inflate(layoutInflater)
        setContentView(b.root)

        b.btnFoto.setOnClickListener {
            elegirFoto.launch(
                PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
            )
        }
        b.btnUbicacion.setOnClickListener { solicitarUbicacion() }
        b.btnGuardar.setOnClickListener { guardar() }
    }

    override fun onStop() {
        cancelacion?.cancel()
        cancelacion = null
        super.onStop()
    }

    private fun tienePermiso() =
        ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) ==
            PackageManager.PERMISSION_GRANTED ||
            ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) ==
            PackageManager.PERMISSION_GRANTED

    private fun solicitarUbicacion() {
        when {
            tienePermiso() -> obtenerUbicacion()
            shouldShowRequestPermissionRationale(Manifest.permission.ACCESS_FINE_LOCATION) ->
                AlertDialog.Builder(this)
                    .setTitle(R.string.permiso_titulo)
                    .setMessage(R.string.permiso_motivo)
                    .setPositiveButton(R.string.continuar) { _, _ -> lanzarPermisos() }
                    .setNegativeButton(R.string.cancelar, null)
                    .show()
            else -> lanzarPermisos()
        }
    }

    private fun lanzarPermisos() {
        pedirPermisos.launch(
            arrayOf(
                Manifest.permission.ACCESS_FINE_LOCATION,
                Manifest.permission.ACCESS_COARSE_LOCATION
            )
        )
    }

    private fun mostrarIrAAjustes() {
        AlertDialog.Builder(this)
            .setTitle(R.string.permiso_titulo)
            .setMessage(R.string.permiso_bloqueado)
            .setPositiveButton(R.string.abrir_ajustes) { _, _ ->
                startActivity(
                    Intent(
                        Settings.ACTION_APPLICATION_DETAILS_SETTINGS,
                        Uri.fromParts("package", packageName, null)
                    )
                )
            }
            .setNegativeButton(R.string.cancelar, null)
            .show()
    }

    @SuppressLint("MissingPermission")
    private fun obtenerUbicacion() {
        b.tvUbicacion.setText(R.string.buscando_ubicacion)
        val cts = CancellationTokenSource().also { cancelacion = it }
        fused.getCurrentLocation(Priority.PRIORITY_HIGH_ACCURACY, cts.token)
            .addOnSuccessListener { loc ->
                if (loc != null) mostrarUbicacion(loc)
                else fused.lastLocation.addOnSuccessListener { ultima ->
                    if (ultima != null) mostrarUbicacion(ultima) else sinUbicacion()
                }
            }
            .addOnFailureListener { sinUbicacion() }
    }

    private fun mostrarUbicacion(loc: Location) {
        ubicacion = loc
        b.tvUbicacion.text = String.format(Locale.US, "%.5f, %.5f", loc.latitude, loc.longitude)
    }

    private fun sinUbicacion() {
        b.tvUbicacion.setText(R.string.sin_ubicacion_aun)
        Toast.makeText(this, R.string.sin_ubicacion, Toast.LENGTH_LONG).show()
    }

    private fun guardar() {
        val nombre = b.etNombre.text.toString().trim()
        val uid = Firebase.auth.currentUser?.uid
        val foto = fotoUri
        val loc = ubicacion
        if (uid == null || nombre.isEmpty() || loc == null) {
            Toast.makeText(this, R.string.faltan_datos, Toast.LENGTH_LONG).show()
            return
        }

        b.btnGuardar.isEnabled = false
        b.progress.visibility = View.VISIBLE

        if (foto == null) {
            guardarEnFirestore(nombre, loc, "", uid)
            return
        }

        val ref = Firebase.storage.reference.child("fotos/$uid/${UUID.randomUUID()}.jpg")
        ref.putFile(foto)
            .continueWithTask { t ->
                if (!t.isSuccessful) throw (t.exception ?: Exception(getString(R.string.error_foto)))
                ref.downloadUrl
            }
            .addOnSuccessListener { url -> guardarEnFirestore(nombre, loc, url.toString(), uid) }
            .addOnFailureListener {
                Toast.makeText(this, R.string.foto_no_subida, Toast.LENGTH_LONG).show()
                guardarEnFirestore(nombre, loc, "", uid)
            }
    }

    private fun guardarEnFirestore(nombre: String, loc: Location, fotoUrl: String, uid: String) {
        val lugar = Lugar(
            nombre = nombre,
            lat = loc.latitude,
            lng = loc.longitude,
            fotoUrl = fotoUrl,
            uid = uid,
            creado = System.currentTimeMillis()
        )
        Firebase.firestore.collection("lugares").add(lugar)
            .addOnSuccessListener { finish() }
            .addOnFailureListener { fallo(it) }
    }

    private fun fallo(e: Exception) {
        b.btnGuardar.isEnabled = true
        b.progress.visibility = View.GONE
        Toast.makeText(this, e.localizedMessage ?: getString(R.string.error_generico), Toast.LENGTH_LONG).show()
    }
}
