"""Physikalische Kurztests der Funktionen direkt aus dem Lehrnotebook.
Ausführen: python validate_md.py (benötigt NumPy).
"""
import json
from pathlib import Path
import numpy as np

nb = json.loads(Path(__file__).with_name('MD_2D_Berendsen.ipynb').read_text())
ns = {'np': np}
for cell in nb['cells']:
    source = ''.join(cell['source'])
    if cell['cell_type'] == 'code' and source.startswith(('def forces', 'def simulate')):
        exec(source, ns)
forces, simulate = ns['forces'], ns['simulate']
r = np.array([[1., 1.], [2.2, 1.3], [4., 4.]])
F, U, W = forces(r, 8.)
assert np.allclose(F.sum(axis=0), 0, atol=1e-12)
# Kraft ist negativer Potentialgradient, fern vom Cutoff.
h = 1e-6
for i in range(len(r)):
    for d in range(2):
        plus, minus = r.copy(), r.copy()
        plus[i, d] += h
        minus[i, d] -= h
        numerical = -(forces(plus, 8.)[1] - forces(minus, 8.)[1]) / (2*h)
        assert np.isclose(F[i, d], numerical, atol=1e-7)
assert np.allclose(forces(r + [8., -8.], 8.)[0], F)
# Paarvirial und ideale kinetische Druckkomponente.
assert np.isclose(W, np.sum(r * F))
v = np.array([[1., 0.], [-1., 0.]])
K, T, P = ns['observables'](v, 8., 0.)
assert np.isclose(T, 1.) and np.isclose(P, K / 64.)
# NVE: kurzfristig kleine Energiedrift und erhaltener Gesamtimpuls.
nve = simulate(steps=2000, dt=0.001, thermostat=False, barostat=False)
relative_drift = np.ptp(nve['total_energy']) / abs(nve['total_energy'][0])
assert relative_drift < 0.005, relative_drift
assert np.linalg.norm(nve['final_velocities'].sum(axis=0)) < 1e-10
assert np.ptp(nve['volume']) == 0
# Ein gekoppelter Schritt: Temperaturrelaxation und 2D-Flächenskalierung.
base = dict(steps=1, sample_every=1, frame_every=1, dt=0.003)
free = simulate(**base, thermostat=False, barostat=False)
therm = simulate(**base, thermostat=True, barostat=False)
expected_T = free['temperature'][1] + 0.003/0.3*(1-free['temperature'][1])
assert np.isclose(therm['temperature'][1], expected_T)
coupled = simulate(**base)
expected_V = therm['volume'][1]*(1 + 0.5*0.003/3*(therm['pressure'][1]-1))
assert np.isclose(coupled['volume'][1], expected_V)
# Speicherung bei nicht teilbarer Schrittzahl und Neuberechnung der Endobservablen.
run = simulate(steps=101, sample_every=10, frame_every=20)
assert run['time'].shape == (11,) and run['trajectory'].shape == (6,64,2)
_, U, W = forces(coupled['final_positions'], coupled['final_L'])
assert np.isclose(U, coupled['potential_energy'][-1])
assert np.isclose(ns['observables'](coupled['final_velocities'], coupled['final_L'], W)[2],
                  coupled['pressure'][-1])
print(f'Alle Tests bestanden; relative NVE-Energiespanne: {relative_drift:.3g}')
