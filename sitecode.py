import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. Sayfa Temel Ayarları
st.set_page_config(
    page_title="Türkiye Güneş Potansiyeli Haritası",
    page_icon="☀️",
    layout="wide"
)

st.title("☀️ Türkiye Güneş Enerjisi ve Potansiyel Haritası")
st.markdown("Harita üzerinden bir il seçerek güneşlenme süresi, ışınım potansiyeli ve santral kurulum alanlarını inceleyebilirsiniz.")

# 2. Türkiye İlleri Güneş Potansiyeli Veri Tabanı (GEPA & Meteoroloji Referanslı)
sehir_verileri = {
    "İl": [
        "Adana", "Ankara", "Antalya", "Aydın", "Balıkesir", "Bursa", 
        "Çanakkale", "Denizli", "Diyarbakır", "Erzurum", "Gaziantep", 
        "Hatay", "İzmir", "Kahramanmaraş", "Kayseri", "Konya", 
        "Malatya", "Mersin", "Muğla", "Samsun", "Sivas", 
        "Şanlıurfa", "Trabzon", "Van", "İstanbul"
    ],
    "lat": [
        37.0000, 39.9334, 36.8969, 37.8560, 39.6484, 40.1885,
        40.1553, 37.7765, 37.9144, 39.9055, 37.0662,
        36.2023, 38.4192, 37.5858, 38.7205, 37.8746,
        38.3552, 36.8121, 37.2153, 41.2867, 39.7477,
        37.1674, 41.0027, 38.5012, 41.0082
    ],
    "lon": [
        35.3213, 32.8597, 30.7133, 27.8416, 27.8826, 29.0610,
        26.4142, 29.0864, 40.2306, 41.2658, 37.3833,
        36.1606, 27.1287, 36.9371, 35.4826, 32.4932,
        38.3095, 34.6415, 28.3636, 36.3300, 37.0179,
        38.7955, 39.7168, 43.3730, 28.9784
    ],
    "Yillik_Gunes_Saati": [
        2950, 2640, 3010, 2920, 2680, 2420,
        2600, 2880, 2980, 2550, 2960,
        2890, 2890, 2840, 2720, 2850,
        2860, 3000, 2950, 1920, 2630,
        3050, 1680, 3080, 2380
    ],
    "Gunes_Isinimi_kWh_m2": [
        1640, 1510, 1680, 1630, 1520, 1420,
        1500, 1620, 1690, 1490, 1660,
        1630, 1610, 1600, 1580, 1620,
        1610, 1670, 1670, 1260, 1530,
        1750, 1150, 1720, 1390
    ],
    "Uygunluk_Derecesi": [
        "Mükemmel", "Yüksek", "Mükemmel", "Çok Yüksek", "Yüksek", "Orta",
        "Yüksek", "Çok Yüksek", "Mükemmel", "Yüksek", "Mükemmel",
        "Çok Yüksek", "Çok Yüksek", "Yüksek", "Yüksek", "Çok Yüksek",
        "Yüksek", "Mükemmel", "Mükemmel", "Düşük", "Yüksek",
        "Mükemmel", "Düşük", "Mükemmel", "Orta"
    ],
    "Uygun_Alanlar": [
        "Çukurova tarım dışı marjinal alanlar, fabrika çatıları",
        "Başkent OSB çatıları, Polatlı-Haymana kırsal arazileri",
        "Sera çatıları, Kumluca-Manavgat kırsal çorak sahalar",
        "Sanayi tesisleri, tarıma elverişsiz güney yamaçlar",
        "Bandırma-Gönen sanayi çatıları ve kırsal alanlar",
        "Nilüfer OSB ve otomotiv sanayi fabrika çatıları",
        "Biga-Ezine sanayi çatıları, marjinal kırsal alanlar",
        "Tekstil fabrikası çatıları, Sarayköy-Çivril arazileri",
        "Bismil-Silvan kırsal marjinal alanları, OSB çatıları",
        "Güneşli yüksek platolar (soğuk hava yüksek panel verimi)",
        "Güneydoğu Anadolu kurak alanları, fıstık işleme tesis çatıları",
        "İskenderun ağır sanayi depo çatıları ve kırsal yamaçlar",
        "Aliağa/Torbalı sanayi çatıları, tarım dışı tepe yamaçları",
        "Tekstil ve çelik sanayi çatıları, Elbistan kırsalı",
        "İncesu/Mimarsinan OSB çatıları, Develi marjinal arazileri",
        "Karapınar Enerji İhtisas Bölgesi, Cihanbeyli kurak düzlükleri",
        "Kuru kayısı işleme tesisleri, organize sanayi çatıları",
        "Tarsus OSB, liman depo çatıları ve kırsal taşlık araziler",
        "Yatağan/Milas atıl maden sahaları, otel-turizm çatıları",
        "Gıda sanayi depo çatıları (öz tüketim odaklı)",
        "Kangal-Şarkışla kırsal arazileri, fabrika çatıları",
        "Geniş düz marjinal tarım dışı araziler, OSB çatıları",
        "Ticari bina çatıları (bölgesel mikro öz tüketim)",
        "Tuşba ve Erciş güneye bakan yüksek verimli soğuk platolar",
        "Lojistik depoları, AVM çatıları, otopark sundurmaları"
    ]
}

df_turkiye = pd.DataFrame(sehir_verileri)

# 3. İki Sütunlu Sayfa Düzeni (Sol: Harita ve Seçim, Sağ: Detay Paneli)
col_harita, col_detay = st.columns([1.3, 1.0])

with col_harita:
    st.subheader("🗺️ Türkiye Güneş Potansiyeli İnteraktif Haritası")
    st.caption("Harita üzerindeki illere yaklaşabilir, noktaların üzerine gelerek veya alttaki kutudan il seçebilirsiniz.")

    # Plotly Scatter Mapbox (Güneş Işınımına Göre Renklendirme)
    fig_map = px.scatter_mapbox(
        df_turkiye,
        lat="lat",
        lon="lon",
        hover_name="İl",
        hover_data={
            "Yillik_Gunes_Saati": True,
            "Gunes_Isinimi_kWh_m2": True,
            "Uygunluk_Derecesi": True,
            "lat": False,
            "lon": False
        },
        color="Gunes_Isinimi_kWh_m2",
        size="Yillik_Gunes_Saati",
        color_continuous_scale="YlOrRd",
        size_max=16,
        zoom=5.0,
        center={"lat": 38.9637, "lon": 35.2433},
        mapbox_style="carto-positron",
        title="İllere Göre Yıllık Işınım (kWh/m²)"
    )
    fig_map.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
    st.plotly_chart(fig_map, use_container_width=True)

    secilen_il = st.selectbox(
        "Detaylı Analizini Görmek İstediğiniz İli Seçin:",
        df_turkiye["İl"].tolist(),
        index=df_turkiye["İl"].tolist().index("Kayseri")
    )

# Seçilen İlin Satırını Getir
il_bilgisi = df_turkiye[df_turkiye["İl"] == secilen_il].iloc[0]

with col_detay:
    st.subheader(f"📍 {secilen_il} Güneş Profili ve Potansiyeli")
    
    # Metrik Kartları
    m1, m2 = st.columns(2)
    m1.metric("☀️ Yıllık Güneşlenme Süresi", f"{il_bilgisi['Yillik_Gunes_Saati']} Saat/Yıl")
    m2.metric("⚡ Yıllık Toplam Işınım", f"{il_bilgisi['Gunes_Isinimi_kWh_m2']} kWh/m²")
    
    st.info(f"**GES Kurulum Uygunluk Seviyesi:** {il_bilgisi['Uygunluk_Derecesi']}")
    
    st.markdown("#### 🏭 Önerilen Kurulum ve Potansiyel Alanlar:")
    st.write(il_bilgisi["Uygun_Alanlar"])

    # Open-Meteo Canlı 7 Günlük Tahmin Grafiği
    st.markdown("---")
    st.markdown(f"#### 🌤️ {secilen_il} İçin 7 Günlük Saatlik Canlı Işınım Grafiği")
    
    @st.cache_data(ttl=3600)
    def sehir_hava_cek(lat, lon):
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=direct_normal_irradiance,diffuse_radiation&forecast_days=7&timezone=auto"
        res = requests.get(api_url).json()
        h_data = res["hourly"]
        df_h = pd.DataFrame({
            "Zaman": pd.to_datetime(h_data["time"]),
            "Toplam_Isinim_W_m2": [d + s for d, s in zip(h_data["direct_normal_irradiance"], h_data["diffuse_radiation"])]
        })
        return df_h

    with st.spinner("Meteoroloji uydusundan canlı ışınım verisi alınıyor..."):
        df_canli = sehir_hava_cek(il_bilgisi["lat"], il_bilgisi["lon"])
        
    fig_line = px.line(
        df_canli, 
        x="Zaman", 
        y="Toplam_Isinim_W_m2", 
        labels={"Toplam_Isinim_W_m2": "Işınım (W/m²)", "Zaman": "Tarih / Saat"},
        color_discrete_sequence=["#FF7F00"]
    )
    fig_line.update_layout(height=260, margin={"r": 0, "t": 10, "l": 0, "b": 0})
    st.plotly_chart(fig_line, use_container_width=True)

# 4. Alt Bölüm: Tüm İllerin Karşılaştırmalı Veri Tablosu
st.markdown("---")
st.subheader("📋 İllere Göre Sıralı Güneş Enerjisi Potansiyel Tablosu")
sirali_tablo = df_turkiye.sort_values(by="Yillik_Gunes_Saati", ascending=False)[
    ["İl", "Yillik_Gunes_Saati", "Gunes_Isinimi_kWh_m2", "Uygunluk_Derecesi", "Uygun_Alanlar"]
]
st.dataframe(sirali_tablo, use_container_width=True)
