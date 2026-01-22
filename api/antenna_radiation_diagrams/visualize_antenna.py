import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

if len(sys.argv) < 2:
    print("Uporaba: python visualize_antenna.py <antenna.az|antenna.el> [rmin_db]")
    print("Primer:  python visualize_antenna.py alfa_868_5dbi.az -30")
    sys.exit(1)

file_path = Path(sys.argv[1])
rmin_db = float(sys.argv[2]) if len(sys.argv) >= 3 else -30.0  # notranji krog (npr. -30 dB)

if not file_path.exists():
    print(f"Napaka: datoteka {file_path} ne obstaja.")
    sys.exit(1)

rotation_deg = 0.0
angles_deg = []
vals = []

with open(file_path, "r") as f:
    for line in f:
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split()

        # SPLAT! .az: prva vrstica je pogosto samo rotacija (1 stolpec)
        if len(parts) == 1 and not angles_deg:
            try:
                rotation_deg = float(parts[0])
                continue
            except ValueError:
                continue

        if len(parts) < 2:
            continue

        try:
            a = float(parts[0])
            v = float(parts[1])
        except ValueError:
            continue

        angles_deg.append(a)
        vals.append(v)

if not angles_deg:
    print("Napaka: ni veljavnih podatkov v datoteki.")
    sys.exit(1)

angles_deg = (np.array(angles_deg) + rotation_deg) % 360.0
vals = np.array(vals, dtype=float)

# pretvorba v dB (ker so .az/.el tipično normalizirane amplitude)
eps = 1e-12
vals = np.clip(vals, eps, None)
gain_db = 20.0 * np.log10(vals)

# (opcijsko) zapri krivuljo, da bo lep krog
order = np.argsort(angles_deg)
angles_deg = angles_deg[order]
gain_db = gain_db[order]
if angles_deg[0] != angles_deg[-1]:
    angles_deg = np.append(angles_deg, angles_deg[0] + 360.0)
    gain_db = np.append(gain_db, gain_db[0])

theta = np.deg2rad(angles_deg)

fig = plt.figure()
ax = fig.add_subplot(111, polar=True)

ax.plot(theta, gain_db)
ax.set_theta_zero_location("N")   # 0° na vrhu
ax.set_theta_direction(-1)        # v smeri urinega kazalca

# radialna skala: zunanji krog 0 dB, znotraj negativno
ax.set_rmax(0.0)
ax.set_rmin(rmin_db)
ax.set_title(f"Antenski diagram v dB ({file_path.name})")

ax.grid(True)
plt.show()
