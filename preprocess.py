def preprocess(sentence, num_vars, MAX_CLAUSE=100, subsumption=False):
    sentence_len = len(sentence)
    #c2l = {index:set(clause) for index, clause in enumerate(sentence)}
    c2l = {index: clause.copy() for index, clause in enumerate(sentence)}
    l2c = {}
    for val in range(1, num_vars+1):
        l2c[val] = set()
        l2c[-val] = set()
    for index, clause in enumerate(sentence):
        for literal in clause:
            l2c[literal].add(index)

    removed_val = []

    # Subsumption
    if subsumption:
        count = 0
        c2l_set = {index: set(clause) for index, clause in enumerate(sentence)}
        for c_idx in range(sentence_len):
            if len(c2l_set[c_idx]) == 1:
                continue
            for literal in c2l_set[c_idx].copy():
                if len(c2l_set[c_idx]) == 1:
                    break
                for c_idx2 in l2c[-literal]:
                    if literal not in c2l_set[c_idx2] and (c2l_set[c_idx2]-{-literal}).issubset(c2l_set[c_idx]):
                        c2l_set[c_idx].remove(literal)
                        c2l[c_idx].remove(literal)
                        l2c[literal].remove(c_idx)
                        count += 1
                        break
        print("subsumption literals:", count)

    # Bounded variable elimination
    if MAX_CLAUSE > 0:
        for val in range(1, num_vars+1):
            if len(l2c[val]) > 0 and len(l2c[val]) <= MAX_CLAUSE and \
                    len(l2c[-val]) > 0 and len(l2c[-val]) <= MAX_CLAUSE:
                common = l2c[val] & l2c[-val]
                if common:
                    for clause_idx in common:
                        for literal in set(c2l[clause_idx]):
                            l2c[literal].remove(clause_idx)
                        del c2l[clause_idx]

                R = []
                old_num_lits = 0
                old_num_lits += sum([len(c2l[c_idx]) for c_idx in l2c[val]])
                old_num_lits += sum([len(c2l[c_idx]) for c_idx in l2c[-val]])
                for clause_idx1 in l2c[val]:
                    for clause_idx2 in l2c[-val]:
                        #new_clause = c2l[clause_idx1] | c2l[clause_idx2]
                        new_clause = set(c2l[clause_idx1]+c2l[clause_idx2])
                        new_clause.remove(val)
                        new_clause.remove(-val)
                        if not new_clause:
                            if len(c2l[clause_idx1]) == 1 and len(c2l[clause_idx2]) == 1:
                                #print(clause_idx1, c2l[clause_idx1], clause_idx2, c2l[clause_idx2])
                                return [[val], [-val]], []
                        if any(-v in new_clause for v in new_clause):
                            continue
                        R.append(new_clause)
                new_num_lits = sum([len(c) for c in R])
                if old_num_lits >= new_num_lits:
                    removed_clause = []
                    #print(val, l2c[val], [c2l[c_idx] for c_idx in l2c[val]],l2c[-val] , [c2l[c_idx] for c_idx in l2c[-val]])
                    for c_idx in l2c[val].copy():
                        for l in c2l[c_idx]:
                            if c_idx in l2c[l]:
                                l2c[l].remove(c_idx)
                        removed_clause.append(c2l[c_idx].copy())
                        del c2l[c_idx]
                    for c_idx in l2c[-val].copy():
                        for l in c2l[c_idx]:
                            if c_idx in l2c[l]:
                                l2c[l].remove(c_idx)
                        removed_clause.append(c2l[c_idx].copy())
                        del c2l[c_idx]
                    for i in range(len(R)):
                        # c2l[i+sentence_len]=R[i].copy()
                        c2l[i+sentence_len] = list(R[i])
                        for l in R[i]:
                            l2c[l].add(i+sentence_len)
                    sentence_len += len(R)

                    removed_val.append((val, removed_clause))
        print("variable elimination vars:", len(removed_val))

    return list(c2l.values()), removed_val


def postprocess(res, removed_val):
    if not res and not removed_val:
        return None
    if not removed_val:
        return res
    res = set(res)

    for (val, removed_clause) in reversed(removed_val):
        res.discard(val)
        res.add(-val)
        for clause in removed_clause:
            if all(-l in res for l in clause):
                res.add(val)
                res.discard(-val)
                break

    return list(res)
