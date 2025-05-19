import time
from utils import read_grid_from_file, print_solution, get_unknown_vars, format_matrix, write_solution_to_file
from solves.pysat_solver import solve_pysat
from solves.brute_force import brute_force_solver
from solves.backtracking import backtrack
from solves.cnf_generator import create_cnf

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(x) for x in row))
    print()


def process(choice):

    grid = []

    if choice not in ["1", "2", "3"]:
        print("Lựa chọn không hợp lệ !!!")
        return
    if choice == "1":
        grid = read_grid_from_file("testcases/input_1.txt")
    elif choice == "2":
        grid = read_grid_from_file("testcases/input_2.txt")
    elif choice == "3":
        grid = read_grid_from_file("testcases/input_3.txt")

    print_matrix(grid)
    cnf = create_cnf(grid)
    num_vars = len(grid) * len(grid[0])

    output_file = f"results/output_{choice}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        # PySAT
        print("=== pysat: ===")
        start = time.perf_counter()
        model = solve_pysat(cnf)
        elapsed = time.perf_counter() - start
        mat_pysat = format_matrix(grid, model)
        f.write("=== pysat: ===\n")
        if model:
            print_solution(mat_pysat, elapsed)
            write_solution_to_file("pysat", mat_pysat, f, elapsed)
        else:
            print("Không tìm thấy kết quả.")
            f.write("Không tìm thấy kết quả.\n")

        # Brute-force
        print("=== brute force: ===")
        unknown_vars = get_unknown_vars(grid)
        start = time.perf_counter()
        model_bf = brute_force_solver(cnf, unknown_vars)
        elapsed = time.perf_counter() - start
        mat_bf = format_matrix(grid, model_bf)
        f.write("=== brute force: ===\n")
        if model_bf:
            print_solution(mat_bf, elapsed)
            write_solution_to_file("brute force", mat_bf, f, elapsed)
        else:
            print("Không có kết quả (Brute Force).\n")
            f.write("Không có kết quả (Brute Force).\n")
            f.write(f"Thời gian chạy: Không xác định\n\n")

        # Backtracking
        print("=== backtracking: ===")
        if choice in ["2", "3"]:
            print("Backtracking: Bỏ qua do thời gian chạy quá lớn.\n")
            f.write("=== backtracking: ===\n")
            f.write("Bỏ qua do thời gian chạy quá lớn.\n\n")
        else:
            start = time.perf_counter()
            model_bt = backtrack(cnf, num_vars)
            elapsed = time.perf_counter() - start
            mat_bt = format_matrix(grid, model_bt)
            f.write("=== backtracking: ===\n")
            if model_bt:
                print_solution(mat_bt, elapsed)
                write_solution_to_file("backtracking", mat_bt, f, elapsed)
            else:
                print("Không có kết quả.")
                f.write("Không có kết quả.\n")
                f.write(f"Thời gian chạy: Không xác định\n")       
        print(f"*** Kết quả đã được ghi trong file /results/output_{choice}.txt ***")

def main():
    stop = 1
    while stop == 1:
        print(" ========== Gem hunter ========== ")
        print("    1. 5x5")
        print("    2. 11x11")
        print("    3. 20x20")
        print("    4. Thoát")
        print("===================================")
        print("Chọn test case (1-3): ", end="")
        choice = input()
        process(choice)
        
        print("\nBạn có muốn tiếp tục không (y/n)? ")
        check = input()
        if check in ["n", "N"]:
            stop = 0
            
        
if __name__ == "__main__":
    main()