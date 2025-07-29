import numpy as np

class VoxelRayCaster:
    def __init__(self, material_grid: np.ndarray, voxel_size: float = 1.0):
        self.material_grid = material_grid
        self.voxel_size = voxel_size
        self.shape = material_grid.shape
        

    def cast_until_hit(self, origins: np.ndarray, directions: np.ndarray):
        active = np.full(len(origins), True)
        outOfBounds = np.full(len(origins), False)
        posVoxCoords = origins / self.voxel_size

        voxelsVisited = np.full((len(origins),3, 10), None, dtype=object)
        distances = np.full((len(origins), 1, 10), None, dtype=object)

        iter = 0
        while np.any(active):
            iter += 1
            currCoords = posVoxCoords[active,:]
            currVoxIdx = np.floor(currCoords).astype(int)
            nextVoxIdx = currVoxIdx.copy()

            dirNeg = (directions[active,:] < 0)
            onBoundary = (currCoords == currVoxIdx)
            nextVoxIdx[(dirNeg & onBoundary)] -= 1

            partActive = np.all((nextVoxIdx >= 0) & (nextVoxIdx < self.shape), axis=1)
            outOfBounds[active][~partActive] = True
            nextMaterial = self.material_grid[nextVoxIdx[partActive][:,0],nextVoxIdx[partActive][:,1],nextVoxIdx[partActive][:,2]]
            inAir = (nextMaterial == 0)
            partActive[partActive] = inAir
            active[active] = partActive
            
            dirPotential = np.full_like(directions[active,:], np.inf)
            dirPos = (directions[active,:] > 0)
            dirNeg = dirNeg[partActive]
            onBoundary = onBoundary[partActive]

            dirPotential[dirPos] = (1 - np.modf(posVoxCoords[active,:][dirPos])[0]) / directions[active,:][dirPos]
            dirPotential[dirNeg & onBoundary] = -1 / directions[active,:][dirNeg & onBoundary]
            dirPotential[dirNeg & ~onBoundary] = - np.modf(posVoxCoords[active,:][dirNeg & ~onBoundary])[0] / directions[active,:][dirNeg & ~onBoundary]

            dirPotential = np.min(dirPotential, axis=1)
            posVoxCoords[active,:] += dirPotential[:,np.newaxis] * directions[active,:]

            voxelsVisited[active,:,iter-1] = currVoxIdx[partActive]
            distances[active,:,iter-1] = dirPotential[partActive]
            distances.append(dirPotential[:,np.newaxis])
            iter += 1

        return posVoxCoords, outOfBounds, np.array(voxelsVisited), np.concatenate(distances)


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