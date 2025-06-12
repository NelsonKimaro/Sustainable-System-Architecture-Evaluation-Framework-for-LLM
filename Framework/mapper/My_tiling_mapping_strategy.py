import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Define device specs
devices = {
    "CPU": {"PEs": 4, "SRAM_KB": 512},
    "GPU": {"PEs": 1024, "SRAM_KB": 65536},
    "TPU": {"PEs": 8192, "SRAM_KB": 131072},
    "FPGA": {"PEs": 256, "SRAM_KB": 16384},
}

# Mixed square + non-square matrix shapes
matrix_shapes = [
    (512, 256, 1024),
    (1024, 1024, 1024),
    (2048, 512, 512),
    (4096, 1024, 512),
    (1024, 2048, 1024),
    (768, 768, 3072),
    (64, 1024, 64),
    (4096, 256, 2048),
]

# Tiling logic
def compute_tile_mapping(device_specs, M, K, N):
    pe_count = device_specs["PEs"]
    sram_kb = device_specs["SRAM_KB"]
    bytes_per_elem = 4
    max_elements = (sram_kb * 1024) // (3 * bytes_per_elem)
    tile_k = 64
    best_tile_m, best_tile_n, best_util = 1, 1, 0

    for tile_m in range(16, 512, 16):
        for tile_n in range(16, 512, 16):
            usage = tile_m * tile_k + tile_k * tile_n + tile_m * tile_n
            if usage <= max_elements:
                tiles_m = int(np.ceil(M / tile_m))
                tiles_n = int(np.ceil(N / tile_n))
                total_tiles = tiles_m * tiles_n
                util = min(1.0, pe_count / total_tiles)
                if util > best_util:
                    best_tile_m, best_tile_n = tile_m, tile_n
                    best_util = util

    tiles_m = int(np.ceil(M / best_tile_m))
    tiles_n = int(np.ceil(N / best_tile_n))
    total_tiles = tiles_m * tiles_n

    return {
        "tile_m": best_tile_m,
        "tile_n": best_tile_n,
        "tile_k": tile_k,
        "total_tiles": total_tiles,
        "PEs": pe_count,
        "utilization": round(best_util, 2)
    }

# Generate summary
summary = []
for M, K, N in matrix_shapes:
    shape_str = f"{M}x{K}*{K}x{N}"
    for device, specs in devices.items():
        result = compute_tile_mapping(specs, M, K, N)
        summary.append({
            "Matrix Shape": shape_str,
            "Device": device,
            "Tile M": result["tile_m"],
            "Tile N": result["tile_n"],
            "Total Tiles": result["total_tiles"],
            "PE Utilization": result["utilization"]
        })

df = pd.DataFrame(summary)

# --- Plotting ---

def plot_bar(metric, ylabel, title):
    plt.figure(figsize=(12, 6))
    for device in df['Device'].unique():
        device_df = df[df['Device'] == device]
        plt.bar([f"{s}\n{device}" for s in device_df['Matrix Shape']],
                device_df[metric], label=device)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.grid(True, axis='y')
    plt.show()

# Plot PE Utilization
plot_bar("PE Utilization", "Utilization (0–1)", "PE Utilization per Matrix Shape per Device")

# Plot Total Tiles
plot_bar("Total Tiles", "Number of Tiles", "Total Tiles per Matrix Shape per Device")

# Plot Tile Area (Tile M × Tile N)
df["Tile Area"] = df["Tile M"] * df["Tile N"]
plot_bar("Tile Area", "Tile Area (M×N)", "Tile Area per Matrix Shape per Device")
