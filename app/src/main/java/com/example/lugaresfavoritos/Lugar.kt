package com.example.lugaresfavoritos

data class Lugar(
    val nombre: String = "",
    val lat: Double = 0.0,
    val lng: Double = 0.0,
    val fotoUrl: String = "",
    val uid: String = "",
    val creado: Long = 0L
)
