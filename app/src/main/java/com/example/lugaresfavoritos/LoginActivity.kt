package com.example.lugaresfavoritos

import android.content.Intent
import android.os.Bundle
import android.util.Patterns
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.lugaresfavoritos.databinding.ActivityLoginBinding
import com.google.firebase.Firebase
import com.google.firebase.FirebaseNetworkException
import com.google.firebase.auth.FirebaseAuthInvalidCredentialsException
import com.google.firebase.auth.FirebaseAuthInvalidUserException
import com.google.firebase.auth.FirebaseAuthUserCollisionException
import com.google.firebase.auth.FirebaseAuthWeakPasswordException
import com.google.firebase.auth.auth

class LoginActivity : AppCompatActivity() {

    private lateinit var b: ActivityLoginBinding
    private val auth = Firebase.auth

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        if (auth.currentUser != null) {
            irAlInicio()
            return
        }

        b = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(b.root)

        b.btnIngresar.setOnClickListener {
            val (email, pass) = leerDatos() ?: return@setOnClickListener
            cargando(true)
            auth.signInWithEmailAndPassword(email, pass)
                .addOnCompleteListener { t -> resultado(t.isSuccessful, t.exception) }
        }

        b.btnRegistrar.setOnClickListener {
            val (email, pass) = leerDatos() ?: return@setOnClickListener
            cargando(true)
            auth.createUserWithEmailAndPassword(email, pass)
                .addOnCompleteListener { t -> resultado(t.isSuccessful, t.exception) }
        }
    }

    private fun leerDatos(): Pair<String, String>? {
        val email = b.etEmail.text.toString().trim()
        val pass = b.etPassword.text.toString()
        if (!Patterns.EMAIL_ADDRESS.matcher(email).matches() || pass.length < 6) {
            Toast.makeText(this, R.string.datos_invalidos, Toast.LENGTH_LONG).show()
            return null
        }
        return email to pass
    }

    private fun resultado(ok: Boolean, error: Exception?) {
        if (ok) {
            irAlInicio()
            return
        }
        cargando(false)
        Toast.makeText(this, traducirError(error), Toast.LENGTH_LONG).show()
    }

    private fun traducirError(e: Exception?): String {
        val mensaje = e?.localizedMessage.orEmpty()
        return when {
            e is FirebaseAuthUserCollisionException -> getString(R.string.error_correo_en_uso)
            e is FirebaseAuthWeakPasswordException -> getString(R.string.error_clave_debil)
            e is FirebaseAuthInvalidUserException -> getString(R.string.error_credenciales)
            e is FirebaseAuthInvalidCredentialsException -> getString(R.string.error_credenciales)
            e is FirebaseNetworkException -> getString(R.string.error_red)
            mensaje.contains("API key", ignoreCase = true) -> getString(R.string.error_api_key)
            mensaje.contains("CONFIGURATION_NOT_FOUND") -> getString(R.string.error_auth_desactivado)
            mensaje.contains("OPERATION_NOT_ALLOWED") -> getString(R.string.error_auth_desactivado)
            mensaje.isNotEmpty() -> mensaje
            else -> getString(R.string.error_generico)
        }
    }

    private fun cargando(activo: Boolean) {
        b.btnIngresar.isEnabled = !activo
        b.btnRegistrar.isEnabled = !activo
        b.progress.visibility = if (activo) View.VISIBLE else View.GONE
    }

    private fun irAlInicio() {
        startActivity(Intent(this, MainActivity::class.java))
        finish()
    }
}
