import numpy as np

class VoxelRayCaster:
    def __init__(self, material_grid: np.ndarray, voxel_size: float = 1.0):
        self.material_grid = material_grid
        self.voxel_size = voxel_size
        self.grid_shape = material_grid.shape

    def cast_until_hit(self, origins: np.ndarray, directions: np.ndarray):
        """
        Casts rays through the voxel grid starting from 'origins' in given 'directions'
        until a voxel with material != 0 is hit or the ray leaves the grid.

        Parameters:
            origins (np.ndarray): Shape (N, 3), start positions of the rays.
            directions (np.ndarray): Shape (N, 3), normalized directions of the rays.

        Returns:
            hit_positions (np.ndarray): The last position each ray visited.
            out_of_bounds (np.ndarray): Boolean mask indicating which rays exited the grid.
        """
        N = origins.shape[0]
        active = np.ones(N, dtype=bool)           # Tracks rays still traversing
        out_of_bounds = np.zeros(N, dtype=bool)   # Tracks rays that left the grid

        # Current floating-point positions in voxel grid space
        voxel_pos = origins / self.voxel_size

        # Main loop: iterate while any ray is still active
        while np.any(active):
            active_pos = voxel_pos[active]
            active_dir = directions[active]

            voxel_idx = np.floor(active_pos).astype(int)
            next_voxel = voxel_idx.copy()

            # Correct for negative direction hitting a voxel boundary
            dir_neg = (active_dir < 0)
            on_boundary = (active_pos == voxel_idx)
            next_voxel[dir_neg & on_boundary] -= 1

            # Check if within bounds
            within_bounds = np.all((next_voxel >= 0) & (next_voxel < self.grid_shape), axis=1)
            active_indices = np.where(active)[0]
            out_of_bounds[active_indices[~within_bounds]] = True

            # Material check
            next_material = np.zeros(len(next_voxel), dtype=int)
            valid_voxels = within_bounds.nonzero()[0]
            if len(valid_voxels) > 0:
                valid_idxs = next_voxel[valid_voxels]
                next_material[valid_voxels] = self.material_grid[
                    valid_idxs[:, 0],
                    valid_idxs[:, 1],
                    valid_idxs[:, 2]
                ]

            # Determine which rays continue
            is_air = (next_material == 0)
            still_active = within_bounds & is_air
            active[active_indices] = still_active

            # Prepare for position update only for remaining active rays
            active_pos = voxel_pos[active]
            active_dir = directions[active]
            modf_pos, _ = np.modf(active_pos)

            # Distance to next voxel boundary in each axis
            t_delta = np.full_like(active_dir, np.inf)

            dir_pos = (active_dir > 0)
            dir_neg = (active_dir < 0)
            on_bound = (modf_pos == 0.0)

            # For positive directions
            t_delta[dir_pos] = (1.0 - modf_pos[dir_pos]) / active_dir[dir_pos]

            # For negative directions
            t_delta[dir_neg & on_bound] = -1.0 / active_dir[dir_neg & on_bound]
            t_delta[dir_neg & ~on_bound] = -modf_pos[dir_neg & ~on_bound] / active_dir[dir_neg & ~on_bound]

            # Step in direction of smallest boundary crossing
            t_min = np.min(t_delta, axis=1)
            voxel_pos[active] += (t_min[:, None] * active_dir)

        return voxel_pos, out_of_bounds



scale = 100
half_scale = scale // 2
materials = np.zeros([scale+1,scale+1,scale+1])

for i in range(scale):
    for j in range(scale):
        for k in range(scale):
            if (half_scale-i)**2 + (half_scale-j)**2 + (half_scale-k)**2 <= (2+half_scale)**2:
                materials[i,j,k] = 1


points = np.array([
    [0,100,0],
    [0,99.5,0],
    [50,50,6],
    [0,50,0]
])
vec1 = np.array([1,-1,0])
vec1 = vec1 / np.linalg.norm(vec1)
vec2 = np.array([0,1,0])
vec2 = vec2 / np.linalg.norm(vec2)
vec3 = np.array([1,-1,1])
vec3 = vec3 / np.linalg.norm(vec3)

dirs = np.array([vec1, vec1, vec2, vec3])

materials = materials.astype(np.int32)
caster = VoxelRayCaster(materials, voxel_size=1.0)

hit_pos, out_of_world = caster.cast_until_hit(points, dirs)
print(hit_pos)