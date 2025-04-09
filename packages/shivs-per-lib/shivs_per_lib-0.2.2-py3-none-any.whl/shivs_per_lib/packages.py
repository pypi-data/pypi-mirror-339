def str_to_int(given_list):
   return [int(i) for i in given_list]


def int_to_str(given_list):
    return [str(i) for i in given_list]


def data_set(type,value):
    data_int = []
    data_float = []
    data_alpha = []
    data_alpha_numeric = []
    data_boolean = []
    

def q_mc():
    def int_list_to_int(lists,bits):
        string=[]
        for i in lists:
            string.append(str(i))
        if len(string) == bits:
            pass
        else:
            string = ['0']*(bits-len(string)) + string
        return ("".join(string))

    def decimal_to_binary(digit,bits):
        remainder_list = []
        quotient = digit
        while  quotient > 0:
            remainder_list.append(quotient%2)
            quotient = quotient//2
        binary_eq = int_list_to_int(remainder_list[::-1],bits)
        return binary_eq

    def group_minterms_by_ones(minterms, num_vars):
        groups = {}
        for m in minterms:
            bin_rep = decimal_to_binary(m, num_vars)
            ones_count = bin_rep.count('1')
            if ones_count not in groups:
                groups[ones_count] = []
            groups[ones_count].append((m, bin_rep))
        
        print("\nStep 1: Initial Grouping of Minterms")
        for k in sorted(groups.keys()):
            print(f"Group {k}: {[b for _, b in groups[k]]}")
        
        return groups

    def find_prime_implicants(groups):
        next_groups = {}
        used = set()
        prime_implicants = set()
        
        print("\nStep 2: Merging Groups")
        sorted_keys = sorted(groups.keys())
        for i in range(len(sorted_keys) - 1):
            group1, group2 = groups[sorted_keys[i]], groups[sorted_keys[i + 1]]
            for (m1, b1) in group1:
                for (m2, b2) in group2:
                    diff = [j for j in range(len(b1)) if b1[j] != b2[j]]
                    if len(diff) == 1:
                        used.add(m1)
                        used.add(m2)
                        merged = b1[:diff[0]] + 'X' + b1[diff[0] + 1:]
                        next_groups.setdefault(sorted_keys[i], []).append((frozenset([m1, m2]), merged))
                        print(f"{b1} + {b2} -> {merged}")
        
        for g in groups.values():
            for m, b in g:
                if m not in used:
                    prime_implicants.add(b)
        
        print("\n-> Prime Implicants Identified")
        for pi in prime_implicants:
            print(pi)
        
        return next_groups, prime_implicants

    def extract_essential_prime_implicants(minterms, prime_implicants):
        table = {m: [] for m in minterms}
        for imp in prime_implicants:
            for m in minterms:
                if all(imp[i] == 'X' or imp[i] == decimal_to_binary(m, len(imp))[i] for i in range(len(imp))):
                    table[m].append(imp)
        
        print("\nStep 3: Prime Implicant Table")
        for m, imps in table.items():
            print(f"Minterm {m}: {imps}")
        
        essential = set()
        for m, imps in table.items():
            if len(imps) == 1:
                essential.add(imps[0])
        
        print("\nStep 4: Essential Prime Implicants Identified")
        for epi in essential:
            print(epi)
        
        return essential

    def binary_to_expression(binary):
        variables = [chr(65 + i) for i in range(len(binary))]
        terms = [variables[i] if binary[i] == '1' else (variables[i] + "'") for i in range(len(binary)) if binary[i] != 'X']
        return ''.join(terms)

    def quine_mccluskey(minterms, dont_cares, num_vars):
        print("\nStarting Quine-McCluskey Method\n")
        all_terms = minterms + dont_cares
        groups = group_minterms_by_ones(all_terms, num_vars)
        next_groups, prime_implicants = find_prime_implicants(groups)
        
        while next_groups:
            next_groups, new_pis = find_prime_implicants(next_groups)
            prime_implicants.update(new_pis)
        
        essential_prime_implicants = extract_essential_prime_implicants(minterms, prime_implicants)
        final_expression = ' + '.join(map(binary_to_expression, essential_prime_implicants))
        
        if not final_expression:
            final_expression = "1"  # If all minterms are covered, return 1
        
        print("\nStep 6: Final Simplified Boolean Expression")
        print("Final Expression:", final_expression)
        return final_expression

    def str_to_int(lst):
        return [int(i) for i in lst]

    minterms = str_to_int(input("Enter Minterms (space-separated): ").split())
    dont_cares = str_to_int(input("Enter Don't-Care Terms (space-separated, or leave blank): ").split() or [])
    num_vars = int(input("Enter number of variables: "))
    quine_mccluskey(minterms, dont_cares, num_vars)
