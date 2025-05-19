from itertools import product

def brute_force_solver(cnf, unknown_vars):
    if not unknown_vars:
        return {} if all(any(lit < 0 for lit in clause) for clause in cnf) else None

    max_combinations = 16_000_000
    if len(unknown_vars) > 24:
        print(f"Cảnh báo: Quá nhiều biến chưa biết ({len(unknown_vars)}). Chỉ thử {max_combinations} tổ hợp.")
        return None

    sorted_cnf = sorted(cnf, key=len)

    forced_true = set()   # Biến bắt buộc là True (bẫy)
    forced_false = set()  # Biến bắt buộc là False (ngốc)
    for clause in sorted_cnf:
        if len(clause) == 1:
            lit = clause[0]
            var = abs(lit)
            if lit > 0:
                forced_true.add(var)
            else:
                forced_false.add(var)

    # Lọc unknown_vars, loại biến đã cố định
    effective_vars = [v for v in unknown_vars if v not in forced_true and v not in forced_false]
    print(f"Số biến chưa biết hiệu quả: {len(effective_vars)}")

    count = 0
    for bits in product([False, True], repeat=len(effective_vars)):
        count += 1
        if count > max_combinations:
            print("Đạt giới hạn tổ hợp. Không tìm thấy lời giải trong giới hạn.")
            return None

        if count % 4_000_000 == 0:
            print(f"Đã thử {count:,} tổ hợp ({count/max_combinations*100:.1f}%)...")

        # Tạo assignment
        assignment = {v: True for v in forced_true}
        assignment.update({v: False for v in forced_false})
        assignment.update({v: bits[i] for i, v in enumerate(effective_vars)})

        # Kiểm tra CNF nhanh
        satisfied = True
        for clause in sorted_cnf:
            if not any(
                (lit > 0 and assignment.get(abs(lit), False)) or
                (lit < 0 and not assignment.get(abs(lit), False))
                for lit in clause
            ):
                satisfied = False
                break
        if satisfied:
            print(f"Tìm thấy lời giải sau {count:,} tổ hợp!")
            return assignment

    print(f"Đã thử {count:,} tổ hợp. Không tìm thấy lời giải.")
    return None
