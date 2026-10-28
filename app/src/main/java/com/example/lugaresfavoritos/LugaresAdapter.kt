package com.example.lugaresfavoritos

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import coil.load
import com.example.lugaresfavoritos.databinding.ItemLugarBinding
import java.util.Locale

class LugaresAdapter : RecyclerView.Adapter<LugaresAdapter.VH>() {

    private var items: List<Lugar> = emptyList()

    class VH(val b: ItemLugarBinding) : RecyclerView.ViewHolder(b.root)

    fun submit(lista: List<Lugar>) {
        items = lista
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        VH(ItemLugarBinding.inflate(LayoutInflater.from(parent.context), parent, false))

    override fun getItemCount() = items.size

    override fun onBindViewHolder(holder: VH, position: Int) {
        val lugar = items[position]
        holder.b.tvNombre.text = lugar.nombre
        holder.b.tvCoords.text = String.format(Locale.US, "%.5f, %.5f", lugar.lat, lugar.lng)
        if (lugar.fotoUrl.isNotEmpty()) {
            holder.b.ivFoto.load(lugar.fotoUrl) {
                crossfade(true)
                placeholder(android.R.drawable.ic_menu_gallery)
                error(android.R.drawable.ic_menu_report_image)
            }
        } else {
            holder.b.ivFoto.setImageResource(android.R.drawable.ic_menu_mapmode)
        }
    }
}
