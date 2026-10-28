package com.example.lugaresfavoritos

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.LatLng
import com.google.android.gms.maps.model.LatLngBounds
import com.google.android.gms.maps.model.MarkerOptions
import com.google.firebase.Firebase
import com.google.firebase.auth.auth
import com.google.firebase.firestore.firestore

class MapaActivity : AppCompatActivity(), OnMapReadyCallback {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_mapa)
        (supportFragmentManager.findFragmentById(R.id.map) as SupportMapFragment).getMapAsync(this)
    }

    override fun onMapReady(map: GoogleMap) {
        val uid = Firebase.auth.currentUser?.uid ?: return
        map.uiSettings.isZoomControlsEnabled = true

        Firebase.firestore.collection("lugares")
            .whereEqualTo("uid", uid)
            .get()
            .addOnSuccessListener { result ->
                val lugares = result.toObjects(Lugar::class.java)
                if (lugares.isEmpty()) {
                    Toast.makeText(this, R.string.sin_lugares, Toast.LENGTH_LONG).show()
                    return@addOnSuccessListener
                }

                val bounds = LatLngBounds.Builder()
                lugares.forEach { l ->
                    val pos = LatLng(l.lat, l.lng)
                    map.addMarker(MarkerOptions().position(pos).title(l.nombre))
                    bounds.include(pos)
                }

                if (lugares.size == 1) {
                    val pos = LatLng(lugares[0].lat, lugares[0].lng)
                    map.moveCamera(CameraUpdateFactory.newLatLngZoom(pos, 15f))
                } else {
                    map.setOnMapLoadedCallback {
                        map.moveCamera(CameraUpdateFactory.newLatLngBounds(bounds.build(), 120))
                    }
                }
            }
            .addOnFailureListener {
                Toast.makeText(this, it.localizedMessage, Toast.LENGTH_LONG).show()
            }
    }
}
