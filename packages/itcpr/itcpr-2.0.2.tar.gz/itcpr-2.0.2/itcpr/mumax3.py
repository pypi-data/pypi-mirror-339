import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import struct
from scipy.interpolate import interp1d
import os
import csv
import glob

def simple_plot(
    filepath,
    components=["mx", "my", "mz"],
    title="Magnetization vs Time",
    xlabel="Time (s)",
    ylabel="Magnetization",
    colors=None,
    labels=None,
    grid=True,
    figsize=(10, 6),
    show=True,
    three_d=False
):
    try:
        # Open file manually, read header line
        with open(filepath, 'r') as f:
            header_line = f.readline().lstrip("#").strip()
            column_names = [col.strip().split()[0] for col in header_line.split('\t')]
    
        # Load data with cleaned column names
        df = pd.read_csv(filepath, sep=r'\s+', engine='python', skiprows=1, names=column_names)
        print("✅ Cleaned columns:", df.columns.tolist())
    except Exception as e:
        raise ValueError(f"❌ Failed to load file {filepath}: {e}")

    if three_d:
        title = 'Magnetization dynamics in 3d'
        if all(col in df.columns for col in ["mx", "my", "mz"]):
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(df["mx"], df["my"], df["mz"], color='blue')
            ax.set_xlabel("Mx")
            ax.set_ylabel("My")
            ax.set_zlabel("Mz")
            ax.set_title(title)
            if grid:
                ax.grid(True)
            if show:
                plt.show()
        else:
            print("⚠️  Cannot plot in 3D. One or more of mx, my, mz not found in columns.")
        return

    # 2D plot path
    time_col = "t"
    time = df[time_col]

    plt.figure(figsize=figsize)

    for i, comp in enumerate(components):
        if comp in df.columns:
            color = colors[i] if colors and i < len(colors) else None
            label = labels[i] if labels and i < len(labels) else comp
            plt.plot(time, df[comp], label=str(label), color=color)
        else:
            print(f"⚠️  Warning: Component '{comp}' not found in columns.")

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xlim([time.min(), time.max()])
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.gca().set_aspect('auto', adjustable='box')
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.axvline(0, color='black', lw=0.5, ls='--')
    plt.axhline(1, color='black', lw=0.5, ls='--')
    plt.axvline(1, color='black', lw=0.5, ls='--')
    plt.axhline(-1, color='black', lw=0.5, ls='--')
    plt.axvline(-1, color='black', lw=0.5, ls='--')
    if grid:
        plt.grid(True)
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()

# mumax_analysis.py
def load_oommf_domfile(filepath, verbose=True):
    HEADER_STR1 = 'OOMMF: rectangular mesh v1.0'
    HEADER_STR2 = '# OOMMF OVF 2.0'

    with open(filepath, 'rb') as f:
        header = f.readline().decode('utf-8').strip()
        if HEADER_STR1 in header:
            ovf_version = 1
        elif HEADER_STR2 in header:
            ovf_version = 2
        else:
            raise ValueError(f"Unknown OVF header format: {header}")

        lines = []
        while True:
            pos = f.tell()
            line = f.readline().decode('utf-8', errors='ignore').strip()
            lines.append(line)
            if 'Begin: Data' in line:
                f.seek(pos)
                break

        def extract(pattern):
            for l in lines:
                if pattern in l:
                    return float(l.split(pattern)[-1].strip())
            return None

        nx, ny, nz = [int(extract(f'{k}:')) for k in ['xnodes', 'ynodes', 'znodes']]
        dx, dy, dz = [extract(f'{k}:') for k in ['xstepsize', 'ystepsize', 'zstepsize']]
        xo, yo, zo = [extract(f'{k}:') for k in ['xbase', 'ybase', 'zbase']]

        dtype = None
        for l in lines:
            if 'Binary 4' in l:
                dtype = 'f'
                break
            elif 'Binary 8' in l:
                dtype = 'd'
                break
            elif 'Text' in l:
                dtype = 'text'
                break

        data = {
            'nx': nx, 'ny': ny, 'nz': nz,
            'dx': dx, 'dy': dy, 'dz': dz,
            'xo': xo, 'yo': yo, 'zo': zo,
        }

        if dtype == 'text':
            while True:
                line = f.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith('# Begin: Data'):
                    break
            vals = []
            for _ in range(nx * ny * nz):
                line = f.readline().decode('utf-8')
                vals.append(list(map(float, line.strip().split())))
            vals = np.array(vals)
            if vals.shape[1] == 3:
                data['Mx'] = vals[:, 0].reshape((nz, ny, nx))
                data['My'] = vals[:, 1].reshape((nz, ny, nx))
                data['Mz'] = vals[:, 2].reshape((nz, ny, nx))
            else:
                data['geom'] = vals[:, 0].reshape((nz, ny, nx))
        else:
            while True:
                line = f.readline().decode('utf-8', errors='ignore')
                if line.startswith('# Begin: Data'):
                    break
            raw = f.read(nx * ny * nz * 3 * struct.calcsize(dtype))
            vals = struct.unpack(f'{nx*ny*nz*3}{dtype}', raw)
            vals = np.array(vals)
            data['Mx'] = vals[0::3].reshape((nz, ny, nx))
            data['My'] = vals[1::3].reshape((nz, ny, nx))
            data['Mz'] = vals[2::3].reshape((nz, ny, nx))

    return data

def load_mumax_txt(filepath):
    with open(filepath, 'r') as f:
        header = f.readline().strip().split('\t')
    data = np.loadtxt(filepath, skiprows=1)
    return data, header

def rearange_mumax_table_output(data, header=None):
    dat = {}
    if header is None and data.shape[1] >= 4:
        dat['# t (s)'] = data[:, 0]
        dat['mx ()'] = data[:, 1]
        dat['my ()'] = data[:, 2]
        dat['mz ()'] = data[:, 3]
    elif header:
        for i, name in enumerate(header):
            dat[name.strip()] = data[:, i]
    else:
        raise ValueError("Insufficient data or header")
    return dat

def perform_simple_fft(x, y, extra_padding=1):
    dt = np.mean(np.diff(x))
    tmax = np.max(x)
    nt = len(x)
    Npts = 2 ** (int(np.ceil(np.log2(nt))) + extra_padding)
    fNy = 1 / (2 * dt)
    df = fNy / (Npts / 2)
    f = np.arange(0, fNy + df, df)

    y_interp = y
    if not np.allclose(np.diff(x), dt, atol=1e-16):
        x_fixed = np.linspace(0, tmax, nt)
        interp_func = interp1d(x, y, kind='linear', fill_value="extrapolate")
        y_interp = interp_func(x_fixed)
        x = x_fixed

    fft_vals = np.fft.fft(y_interp, n=Npts)
    fft_trim = fft_vals[:len(f)]
    return f, fft_trim

def perform_fft_mumax_output(dat, fft_params, plot_flag=True, save_prefix=None):
    out = {}
    out['t'] = dat['# t (s)']
    out['mx'] = dat['mx ()']
    out['my'] = dat['my ()']
    out['mz'] = dat['mz ()']

    f, fft_mx = perform_simple_fft(dat['# t (s)'], dat['mx ()'], fft_params.get('extra_padding', 1))
    _, fft_my = perform_simple_fft(dat['# t (s)'], dat['my ()'], fft_params.get('extra_padding', 1))
    _, fft_mz = perform_simple_fft(dat['# t (s)'], dat['mz ()'], fft_params.get('extra_padding', 1))

    out['f'] = f
    out['fft_mx'] = fft_mx
    out['fft_my'] = fft_my
    out['fft_mz'] = fft_mz

    if plot_flag:
        plt.figure()
        plt.subplot(2, 2, 1)
        plt.plot(dat['# t (s)'], dat['mx ()']); plt.xlabel('Time'); plt.ylabel('mx')
        plt.subplot(2, 2, 2)
        plt.plot(dat['# t (s)'], dat['my ()']); plt.xlabel('Time'); plt.ylabel('my')
        plt.subplot(2, 2, 3)
        plt.plot(dat['# t (s)'], dat['mz ()']); plt.xlabel('Time'); plt.ylabel('mz')
        plt.tight_layout()
        if save_prefix:
            plt.savefig(f"{save_prefix}_m_vs_t_check.png", dpi=300)

        plt.figure()
        plt.plot(f, np.abs(fft_mz))
        plt.xlabel('Frequency (GHz)'); plt.ylabel('Amplitude')
        plt.title('FFT of Mz')
        plt.grid(True)
        if save_prefix:
            plt.savefig(f"{save_prefix}_fft_peaks.png", dpi=300)

    if save_prefix:
        with open(f"{save_prefix}_fft_output.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['f', 'abs_fft_mx', 'arg_fft_mx', 'abs_fft_my', 'arg_fft_my', 'abs_fft_mz', 'arg_fft_mz'])
            for i in range(len(f)):
                row = [f[i], abs(fft_mx[i]), np.angle(fft_mx[i]),
                       abs(fft_my[i]), np.angle(fft_my[i]),
                       abs(fft_mz[i]), np.angle(fft_mz[i])]
                writer.writerow(row)

    return out


def func_do_fk_fft_of_m_vs_xt(folder, file_prefix, title, save_prefix, extra_padding=2, fmax=25, kmax=40):
    files = sorted(glob.glob(os.path.join(folder, file_prefix + '*.ovf')))
    mdata_list = []
    for file in files:
        dat = load_oommf_domfile(file, verbose=False)
        mdata_list.append(dat['mz ()'][0])  # assuming layer 0 (2D)

    m_stack = np.stack(mdata_list, axis=0)  # shape: (nt, ny, nx)
    nt, ny, nx = m_stack.shape
    m_xt = m_stack[:, ny // 2, :]  # take a 1D line at the center y

    t = np.linspace(0, nt, nt)  # dummy time steps (uniform)
    x = np.linspace(0, nx, nx)

    f, fft_t = perform_simple_fft(t, m_xt.T, extra_padding)
    k, fft_k = perform_simple_fft(x, m_xt, extra_padding)

    # 2D FFT (space-time)
    fk_fft = np.fft.fft2(m_xt, s=[len(f), len(k)])
    fk_abs = np.abs(np.fft.fftshift(fk_fft))

    f_axis = np.fft.fftshift(np.fft.fftfreq(len(f), d=(t[1]-t[0])))
    k_axis = np.fft.fftshift(np.fft.fftfreq(len(k), d=(x[1]-x[0])))

    # Save CSVs
    np.savetxt(f"{save_prefix}_mz1_mFFT2.csv", fk_abs, delimiter=',')
    np.savetxt(f"{save_prefix}_freq_mFFT2.csv", f_axis, delimiter=',')
    np.savetxt(f"{save_prefix}_k_mFFT2.csv", k_axis, delimiter=',')

    # Plot
    plt.figure(figsize=(6, 4))
    plt.imshow(fk_abs, extent=[k_axis[0], k_axis[-1], f_axis[0], f_axis[-1]], origin='lower', aspect='auto')
    plt.colorbar(label='|FFT(Mz)|')
    plt.xlabel('k [1/μm]')
    plt.ylabel('f [GHz]')
    plt.title(f"2D FFT of Mz: {title}")
    plt.savefig(f"{save_prefix}_2dfft.png", dpi=300)
    plt.close()

    return f_axis, k_axis, fk_abs
