package com.example.lugaresfavoritos

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.lugaresfavoritos.databinding.ActivityMainBinding
import com.google.firebase.Firebase
import com.google.firebase.auth.auth
import com.google.firebase.firestore.ListenerRegistration
import com.google.firebase.firestore.firestore

class MainActivity : AppCompatActivity() {

    private lateinit var b: ActivityMainBinding
    private val adapter = LugaresAdapter()
    private var registro: ListenerRegistration? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        if (Firebase.auth.currentUser == null) {
            irALogin()
            return
        }

        b = ActivityMainBinding.inflate(layoutInflater)
        setContentView(b.root)

        b.rvLugares.layoutManager = LinearLayoutManager(this)
        b.rvLugares.adapter = adapter

        b.btnNuevo.setOnClickListener {
            startActivity(Intent(this, NuevoLugarActivity::class.java))
        }
        b.btnMapa.setOnClickListener {
            startActivity(Intent(this, MapaActivity::class.java))
        }
        b.btnSalir.setOnClickListener {
            Firebase.auth.signOut()
            irALogin()
        }
    }

    override fun onStart() {
        super.onStart()
        val uid = Firebase.auth.currentUser?.uid ?: return

        registro = Firebase.firestore.collection("lugares")
            .whereEqualTo("uid", uid)
            .addSnapshotListener { snapshot, error ->
                if (error != null) {
                    Toast.makeText(this, error.localizedMessage, Toast.LENGTH_LONG).show()
                    return@addSnapshotListener
                }
                val lista = snapshot?.toObjects(Lugar::class.java).orEmpty()
                adapter.submit(lista.sortedByDescending { it.creado })
                b.tvVacio.visibility = if (lista.isEmpty()) View.VISIBLE else View.GONE
            }
    }

    override fun onStop() {
        registro?.remove()
        registro = null
        super.onStop()
    }

    private fun irALogin() {
        startActivity(Intent(this, LoginActivity::class.java))
        finish()
    }
}
