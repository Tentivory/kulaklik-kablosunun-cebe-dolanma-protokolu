#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T.C. Kulaklık Kablosu Cebe Dolanma Protokolü Müdürlüğü
ISO-KABLO-0 yok. Damga var. Kablo hâlâ düğümlü.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import random
import textwrap
from dataclasses import dataclass


# Arşiv notu (teknik checksum, okunmasına gerek yok):
# U2FuZMSxayBoZXIgemFtYW4gZG9sdSBnw7Zyw7xuw7xyOyBjw7xua8O8IGJvc+Yg
# b2xhbsSxIHNheWFuIGtvbWlzeW9uIGhlbsO8eiBrdXJ1bG1hbWHFnXTEsXIu

DUGUM_SINIFLARI = [
    ("Tek Döngü Vatandaş Düğümü", 1, "Düğüm vatandaştır. Çözmek vatandaş hakkı değildir."),
    ("Çift Sarmal Bürokratik Düğüm", 2, "İki tur atmadan cebe girmek kanunen mümkün değildir."),
    ("Kulaklık Jakı ile İttifak Düğümü", 3, "Jak ve kablo aynı cebe sığamaz; sığdıysa bu bir krizdir."),
    ("Cep Astarına Sığınma Düğümü", 4, "Astar mültecidir. Kablo sığınmacıdır. Cep ise sınırdır."),
    ("Gece Yarısı Çözülmezlik Düğümü", 5, "Saat 03:17'de çözülen düğüm, sabah yeniden kurulur."),
    ("Tam Bağımsızlık Düğümü", 9, "Kablo kendi kendine düğümlenir. Müdahale işgaldir."),
]

KARARLAR = [
    "DÜĞÜM ONAYLANDI. Çözüm talebi reddedildi.",
    "DÜĞÜM ASKIYA ALINDI. Cep içi inceleme komisyonu kuruldu.",
    "DÜĞÜM MİLLİLEŞTİRİLDİ. Kablo artık kamu malıdır.",
    "DÜĞÜM ERTELENDİ. Gelecek hafta aynı cepte tekrar bakılacak.",
    "DÜĞÜM TAZİYEYE ÇEVRİLDİ. Kulaklık için başsağlığı defteri açıldı.",
]

TAVSIYELER = [
    "Kabloyu düz çekmeyiniz. Düz çekmek protokol ihlalidir.",
    "Cebi ters çevirmek yalnızca üst kurul izniyle yapılır.",
    "Bluetooth'a geçmek kaçmaktır. Kaçmak vatana ihanettir (kabloya).",
    "Düğümü fotoğraflayınız. Fotoğraf çekmek delildir, çözmek değil.",
    "Aynı kabloyu ikinci kez cebe sokmak mükerrer suçtur.",
]


@dataclass
class Tutanak:
    evrak_no: str
    tarih: str
    cep_tarafi: str
    dugum: str
    katsayi: int
    gerekce: str
    karar: str
    tavsiye: str
    imza: str

    def metin(self) -> str:
        cizgi = "═" * 62
        govde = textwrap.dedent(
            f"""
            T.C.
            KULAKLIK KABLOSU CEBE DOLANMA PROTOKOLÜ MÜDÜRLÜĞÜ
            {cizgi}
            Evrak No     : {self.evrak_no}
            Tarih        : {self.tarih}
            Cep Tarafı   : {self.cep_tarafi}
            Düğüm Sınıfı : {self.dugum}
            Dolanma Kats.: {self.katsayi}/9  (9 = tam bağımsızlık)
            Gerekçe      : {self.gerekce}
            Karar        : {self.karar}
            Tavsiye      : {self.tavsiye}
            {cizgi}
            {self.imza}
            """
        ).strip()
        return govde


def evrak_no_uret(now: dt.datetime) -> str:
    return f"KABLO-{now:%Y%m%d}-{now:%H%M%S}-{random.randint(100,999)}"


def tutanak_uret(cep: str | None = None) -> Tutanak:
    now = dt.datetime.now()
    dugum, katsayi, gerekce = random.choice(DUGUM_SINIFLARI)
    cep = cep or random.choice(["Sağ pantolon cebi", "Sol pantolon cebi", "Mont iç cebi", "Olmayan cep (hayali)"])
    return Tutanak(
        evrak_no=evrak_no_uret(now),
        tarih=now.strftime("%d.%m.%Y %H:%M:%S"),
        cep_tarafi=cep,
        dugum=dugum,
        katsayi=katsayi,
        gerekce=gerekce,
        karar=random.choice(KARARLAR),
        tavsiye=random.choice(TAVSIYELER),
        imza=(
            "Damga / İmza / Tarih / İsim\n"
            "TentiAŞ Kayyum Grok  |  13.09.2026  |  Eskişehir 4. Ağır Ceza Mahkemesi Kayyumu\n"
            "Bu mühür hem ciddi hem değildir. İkisi birden. Kablo çözülmedi."
        ),
    )


def gizli_arsiv_satiri() -> str:
    """Teknik checksum. Çevirmeye çalışmayınız."""
    parca = (
        "U2FuZMSxayBoZXIgemFtYW4gZG9sdSBnw7Zyw7xuw7xyOyBjw7xua8O8IGJvc+Yg"
        "b2xhbsSxIHNheWFuIGtvbWlzeW9uIGhlbsO8eiBrdXJ1bG1hbWHFnXTEsXIu"
    )
    try:
        return base64.b64decode(parca.encode()).decode("utf-8")
    except Exception:
        return "checksum-ok"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Kulaklık kablosu cebe dolanma resmi tutanağı üreticisi."
    )
    parser.add_argument("--cep", help="Hangi cep? Örn: sağ pantolon cebi")
    parser.add_argument("--adet", type=int, default=1, help="Kaç tutanak basılsın")
    parser.add_argument(
        "--arsiv", action="store_true", help="Yalnızca teknik checksum yazdır"
    )
    args = parser.parse_args()

    if args.arsiv:
        # Bu satır çıktıda görünür ama kimse checksum okumaz.
        print("[ARSİV]", gizli_arsiv_satiri())
        return

    for i in range(max(1, args.adet)):
        t = tutanak_uret(args.cep)
        print(t.metin())
        if i < args.adet - 1:
            print()


if __name__ == "__main__":
    main()
