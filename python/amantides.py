import numpy as np

def traverse_voxels(grid, origin, direction, voxel_size):
    grid_shape = grid.shape
    voxel_size = np.array(voxel_size, dtype=float)
    direction = np.array(direction, dtype=float)
    origin = np.array(origin, dtype=float)

    if np.all(direction == 0):
        raise ValueError("Direction vector must not be zero.")

    # Voxel-Startindex berechnen
    current_voxel = np.floor(origin / voxel_size).astype(int)
    visited_voxels = []
    voxel_distances = []

    # Initiale Prüfung
    def is_inside(voxel_idx):
        return np.all((0 <= voxel_idx) & (voxel_idx < grid_shape))

    if not is_inside(current_voxel):
        return visited_voxels, voxel_distances  # start already outside grid

    # Prüfe direkt Start-Voxel
    if grid[tuple(current_voxel)] != 0:
        visited_voxels.append(tuple(current_voxel))
        voxel_distances.append(0.0)
        return visited_voxels, voxel_distances

    # Schritt-Richtungen
    step = np.sign(direction).astype(int)

    # Vermeide Division durch Null
    inv_dir = np.where(direction != 0, 1.0 / direction, np.inf)

    # Position der nächsten Voxelgrenzen
    next_voxel_boundary = (
        (current_voxel + (step > 0)) * voxel_size
    )

    tMax = np.where(direction != 0,
                    (next_voxel_boundary - origin) * inv_dir,
                    np.inf)

    tDelta = np.abs(voxel_size * inv_dir)

    t = 0.0  # Laufzeit / Strecke

    # Main loop
    while is_inside(current_voxel):
        visited_voxels.append(tuple(current_voxel))

        # Wenn Voxel einen Wert ≠ 0 hat, abbrechen
        if grid[tuple(current_voxel)] != 0:
            break

        # Nächste Achse bestimmen (wo tMax am kleinsten ist)
        axis = np.argmin(tMax)
        dt = tMax[axis] - t
        voxel_distances.append(dt)
        t = tMax[axis]
        tMax[axis] += tDelta[axis]
        current_voxel[axis] += step[axis]

    return visited_voxels, voxel_distances


grid = np.zeros((10, 10, 10), dtype=int)
grid[5, 5, 5] = 1  # Hindernis

origin = [2.5, 2.5, 2.5]
direction = [1, 1, 1]
voxel_size = [1.0, 1.0, 1.0]

voxels, distances = traverse_voxels(grid, origin, direction, voxel_size)

print("Besuchte Voxel:", voxels)
print("Distanzen:", distances)
