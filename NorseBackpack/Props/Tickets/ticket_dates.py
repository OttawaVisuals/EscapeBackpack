"""Departure dates for every travel ticket (designer, 19 Oct 2026).

One calendar for the whole final puzzle: 8 Sep -> 12 Dec 2025, every stop 1-7 days. Keyed by
service number (unique across the 18 hop tickets). The three connecting bookings keep their
booking refs and day pattern; their segment dates are listed here too.
"""

# service number -> departure date, as printed
HOP_DATES = {
    "LF 11":   "08 SEP 2025",   # Leif: L'Anse aux Meadows -> Battle Harbour
    "NA 722":  "11 SEP 2025",   # Battle Harbour -> Brattahlid
    "NA 730":  "17 SEP 2025",   # Brattahlid -> Qikiqtarjuaq
    "VR 6120": "28 SEP 2025",   # Rollo: Walcheren -> Chalus
    "VR 3340": "30 SEP 2025",   # Chalus -> Rouen
    "VR 3412": "07 OCT 2025",   # Rouen -> Bayeux
    "LF 204":  "10 OCT 2025",   # Bayeux -> Winchester
    "VR 5530": "15 OCT 2025",   # Winchester -> Battle
    "VR 5588": "16 OCT 2025",   # Battle -> Roumare Forest
    "LB 31":   "24 OCT 2025",   # Aud: Dogurdarnes -> Hvammur
    "LB 47":   "26 OCT 2025",   # Hvammur -> Bjarnarhofn
    "LB 52":   "01 NOV 2025",   # Bjarnarhofn -> Esjuberg
    "LF 810":  "14 NOV 2025",   # Harald: Oslo -> Staraya Ladoga (a whole week in Oslo, card H1)
    "VR 9021": "20 NOV 2025",   # Staraya Ladoga -> Kyiv
    "LF 377":  "27 NOV 2025",   # Kyiv -> Constantinople
    "NA 455":  "02 DEC 2025",   # Constantinople -> Hedeby
    "NA 463":  "05 DEC 2025",   # Hedeby -> Aci Castello
    "LB 90":   "12 DEC 2025",   # Aci Castello -> Patara
}

# booking ref -> {service: date}
BOOKING_DATES = {
    "RX7T2Q": {"NA 501": "21 SEP 2025", "NA 140": "21 SEP 2025",
               "NA 672": "22 SEP 2025", "VR 2214": "23 SEP 2025"},
    "M4KD8B": {"VR 3312": "20 OCT 2025", "VR 3350": "20 OCT 2025",
               "NA 543": "21 OCT 2025", "LB 58": "21 OCT 2025"},
    "QN2V6H": {"LB 12": "06 NOV 2025", "NA 318": "07 NOV 2025"},
}
