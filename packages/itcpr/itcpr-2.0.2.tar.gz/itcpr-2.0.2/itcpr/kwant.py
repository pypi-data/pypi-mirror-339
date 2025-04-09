import os
import time
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import kwant
import numpy as np

def simulate(
    syst,
    energies,
    main_file="main.py",
    transmission_pairs=[(1, 0)],
    labels=None,
    plot=True,
    save_csv=True,
    save_fig=True,
    save_structure=True,
    save_ldos=False,
    save_wavefunction=False,
    save_current=False,
    save_lead_bands=False,
    selected_energy_for_local=0.1
):
    base_name = os.path.splitext(os.path.basename(main_file))[0]
    out_dir = f"{base_name}.out"
    os.makedirs(out_dir, exist_ok=True)

    log_path = os.path.join(out_dir, f"{base_name}.log")
    fig_path = os.path.join(out_dir, f"{base_name}_conductance.png")
    csv_path = os.path.join(out_dir, f"{base_name}_conductance.csv")
    struct_path = os.path.join(out_dir, f"{base_name}_structure.png")

    def log(msg):
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
        with open(log_path, "a") as f:
            f.write(f"{timestamp} {msg}\n")

    def save_array_to_csv(array, headers, path):
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for i, val in enumerate(array):
                writer.writerow([i, val])
        log(f"CSV saved to {path}")

    log("Simulation started.")

    if isinstance(syst, kwant.builder.Builder):
        syst = syst.finalized()
        log("System finalized.")

    if labels is None:
        labels = [f"T({out},{in_})" for out, in_ in transmission_pairs]

    transmissions = {label: [] for label in labels}

    for energy in energies:
        smatrix = kwant.smatrix(syst, energy)
        for label, (out_lead, in_lead) in zip(labels, transmission_pairs):
            transmissions[label].append(smatrix.transmission(out_lead, in_lead))

    if save_csv:
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Energy [t]"] + labels)
            for i in range(len(energies)):
                row = [energies[i]] + [transmissions[label][i] for label in labels]
                writer.writerow(row)
        log(f"Conductance CSV saved to {csv_path}")

    if save_fig or plot:
        plt.figure()
        for label in labels:
            plt.plot(energies, transmissions[label], label=label)
        plt.xlabel("energy [t]")
        plt.ylabel("conductance [e^2/h]")
        plt.title("Conductance vs Energy")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        if save_fig:
            plt.savefig(fig_path)
            log(f"Conductance plot saved to {fig_path}")
        if plot:
            plt.show()

    if save_structure:
        kwant.plot(syst, file=struct_path, show=False)
        log(f"Structure plot saved to {struct_path}")

    if save_ldos:
        ldos = kwant.ldos(syst, selected_energy_for_local)
        ldos_path = os.path.join(out_dir, f"{base_name}_ldos.png")
        kwant.plot(ldos, file=ldos_path, show=False, colorbar=True)
        log(f"LDOS plot saved to {ldos_path}")

        # Save LDOS CSV
        ldos_csv = os.path.join(out_dir, f"{base_name}_ldos.csv")
        save_array_to_csv(ldos, ["site_index", "ldos"], ldos_csv)

    if save_wavefunction:
        wf = kwant.wave_function(syst, selected_energy_for_local)
        psi = wf(0)[0]
        wf_path = os.path.join(out_dir, f"{base_name}_wavefunction.png")
        kwant.plot(abs(psi)**2, file=wf_path, show=False, colorbar=True)
        log(f"Wavefunction plot saved to {wf_path}")

        # Save Wavefunction CSV
        wf_csv = os.path.join(out_dir, f"{base_name}_wavefunction.csv")
        save_array_to_csv(abs(psi)**2, ["site_index", "probability"], wf_csv)

    if save_current:
        wf = kwant.wave_function(syst, selected_energy_for_local)
        psi = wf(0)[0]
        current_op = kwant.operator.Current(syst)
        current = current_op(psi)
        current_path = os.path.join(out_dir, f"{base_name}_current.png")
        kwant.plot(current, file=current_path, show=False, width=0.05)
        log(f"Current plot saved to {current_path}")

        # Save Current CSV
        current_csv = os.path.join(out_dir, f"{base_name}_current.csv")
        save_array_to_csv(current, ["hopping_index", "current"], current_csv)

    if save_lead_bands:
        bands_path = os.path.join(out_dir, f"{base_name}_lead_bands.png")
        kwant.plotter.bands(syst.leads[0], file=bands_path, show=False)
        log(f"🎶 Lead band structure plot saved to {bands_path}")

    log("Simulation complete.\n")
    return transmissions
