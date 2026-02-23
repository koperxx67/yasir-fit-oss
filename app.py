import os, sys, random
from datetime import datetime, timedelta
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.shortcuts import render, redirect
from django.urls import path

# ==========================================
# 🛡️ YASİR FIT OS: OMEGA PROTOKOLÜ (2X GÜÇ)
# ==========================================
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='yasir-fit-os-omega-2x-master-key',
        ROOT_URLCONF=__name__,
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'whitenoise.middleware.WhiteNoiseMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
        ],
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(os.path.dirname(__file__), 'templates')],
        }],
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.sessions',
        ],
    )

BASLANGIC_TARIHI = datetime(2026, 2, 23)

# 🧠 SİSTEM HAFIZASI (Sohbet ve Veri Deposu)
SYSTEM_STORAGE = {
    'profil': {'yasir_kilo': 110.0, 'hedef': 90.0, 'baslangic': 118.0},
    'finans': {'aylik_butce': 28400, 'harcanan': 4250},
    'gunluk_log': {str(i): {'su': 0, 'kalori': 2200} for i in range(1, 69)},
    'sohbet_gecmisi': [
        {'kim': 'AI', 'mesaj': 'Komutan Yasir, Xoom operasyonu için hazırım. Hedef 90 kg. Emirlerini bekliyorum!', 'zaman': '08:00'}
    ]
}

# 🤖 YAPAY ZEKA CEVAP MOTORU (Senin İçin Özel)
def ai_cevap_uret(mesaj):
    mesaj = mesaj.lower()
    if 'su' in mesaj:
        return "Su hayattır Yasir! 5 litreyi tamamlamadan o yatağa girmek yok!"
    elif 'kilo' in mesaj or 'tartı' in mesaj:
        return f"Şu an {SYSTEM_STORAGE['profil']['yasir_kilo']} kilosun. 90 kiloya az kaldı, o yağlar ağlayarak vücudunu terk edecek!"
    elif 'xoom' in mesaj or 'spor' in mesaj or 'antrenman' in mesaj:
        return "Xoom salonundaki o ağırlıklar senden korksun. Bugün o salona gir ve limitleri zorla Aslanım!"
    elif 'pes' in mesaj or 'yoruldum' in mesaj:
        return "Pes etmek Yasir'in kitabında yazmaz! Kalk ve o seti tamamla!"
    else:
        cevaplar = [
            "Anlaşıldı Komutanım. Kayıtlara geçiyorum.",
            "Türkiye'nin gücünü göster onlara! Basmaya devam!",
            "Senin iraden o çelik barlardan daha sert Yasir. Odaklan!",
            "Operasyon kusursuz ilerliyor. Durmak yok, savaşa devam."
        ]
        return random.choice(cevaplar)

# ==========================================
# ⚙️ GÖRÜNÜM VE İŞLEM YÖNETİCİLERİ
# ==========================================
def main_handler(request):
    gun_no = request.GET.get('gun', str((datetime.now() - BASLANGIC_TARIHI).days + 1))
    sayfa = request.GET.get('p', 'dashboard')
    
    su_verisi = SYSTEM_STORAGE['gunluk_log'].get(gun_no, {'su': 0})
    
    context = {
        'aktif_gun': gun_no,
        'sayfa': sayfa,
        'storage': SYSTEM_STORAGE,
        'su_ml': su_verisi['su'],
        'su_yuzde': min(int((su_verisi['su'] / 5000) * 100), 100),
        'kalan_gun': 68 - int(gun_no),
        'ilerleme': int(((SYSTEM_STORAGE['profil']['baslangic'] - SYSTEM_STORAGE['profil']['yasir_kilo']) / 28) * 100),
        'sohbet': SYSTEM_STORAGE['sohbet_gecmisi']
    }
    return render(request, 'dashboard.html', context)

# 🚀 İŞLEM MERKEZİ (SU HATASI BURADA ÇÖZÜLDÜ)
def islem_handler(request):
    if request.method == "POST":
        gun = request.POST.get('gun', '1')
        islem = request.POST.get('islem')
        suanki_zaman = datetime.now().strftime('%H:%M')
        
        if islem == 'su_ekle':
            SYSTEM_STORAGE['gunluk_log'][gun]['su'] += int(request.POST.get('miktar', 0))
            SYSTEM_STORAGE['sohbet_gecmisi'].append({'kim': 'AI', 'mesaj': f'Tebrikler! Sisteme {request.POST.get("miktar")} ml su girişi yapıldı. Hidrasyon artıyor!', 'zaman': suanki_zaman})
        
        elif islem == 'kilo_set':
            yeni_kilo = float(request.POST.get('kilo', 110.0))
            SYSTEM_STORAGE['profil']['yasir_kilo'] = yeni_kilo
            SYSTEM_STORAGE['sohbet_gecmisi'].append({'kim': 'AI', 'mesaj': f'Yeni tartı verisi alındı: {yeni_kilo} kg. Hedefe bir adım daha!', 'zaman': suanki_zaman})
            
        elif islem == 'sohbet_et':
            kullanici_mesaji = request.POST.get('mesaj', '')
            if kullanici_mesaji:
                SYSTEM_STORAGE['sohbet_gecmisi'].append({'kim': 'Yasir', 'mesaj': kullanici_mesaji, 'zaman': suanki_zaman})
                ai_yaniti = ai_cevap_uret(kullanici_mesaji)
                SYSTEM_STORAGE['sohbet_gecmisi'].append({'kim': 'AI', 'mesaj': ai_yaniti, 'zaman': suanki_zaman})

    return redirect(f'/?gun={request.POST.get("gun", "1")}&p={request.POST.get("p", "dashboard")}')

# ==========================================
# 🌐 URL YÖNLENDİRMELERİ (KUSURSUZ ROTA)
# ==========================================
urlpatterns = [
    path('', main_handler),
    path('islem/', islem_handler), # Eğik çizgi hatası için zırhlı yol
]

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)