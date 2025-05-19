
def read_grid_from_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    grid = []
    for line in lines:
        row = []
        for val in line.strip().split(","):
            val = val.strip()
            if val == "_":
                row.append("_")
            elif val.isdigit():
                row.append(int(val))
            elif val in ["T", "G"]:
                row.append(val)
        grid.append(row)
    return grid

def get_neighbors(grid, i, j):
    rows, cols = len(grid), len(grid[0])
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            ni, nj = i + dx, j + dy
            if (dx != 0 or dy != 0) and 0 <= ni < rows and 0 <= nj < cols:
                neighbors.append((ni, nj))
    return neighbors

def get_unknown_vars(grid):
    rows, cols = len(grid), len(grid[0])
    unknown_vars = []
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '_':
                unknown_vars.append(var(i, j, cols))
    return unknown_vars

def var(i, j, cols):
    return i * cols + j + 1

def format_matrix(grid, model):
    rows, cols = len(grid), len(grid[0])
    mat = []
    for i in range(rows):
        row = []
        for j in range(cols):
            var_num = i * cols + j + 1
            # Xác định giá trị biến
            if isinstance(model, dict):
                val = model.get(var_num, False)
            elif isinstance(model, (list, tuple)):
                if isinstance(model[0], bool):
                    val = model[var_num - 1]
                else:
                    val = var_num in model
            else:
                val = False
            # Gán ký hiệu hiển thị
            if grid[i][j] == "_":
                row.append("T" if val else "G")
            else:
                row.append(str(grid[i][j]))
        mat.append(row)
    return mat

def print_solution(mat, elapsed):
    for row in mat:
        print(" ".join(row))
    print(f"Thời gian chạy: {elapsed:.5f}s\n")

def write_solution_to_file(title, mat, f, elapsed):
    f.write(f"{title}:\n")
    for row in mat:
        f.write(", ".join(row) + "\n")
    f.write(f"Thời gian chạy: {elapsed:.5f}s\n\n")