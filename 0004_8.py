import os
from collections import Counter
import pyfiglet
import termtables as tt


def append_dot(a):
    jj = a.replace("->", "->.")
    return jj


def compress_name(name: str):
    res = Counter(name)
    comp = ''
    for r in res:
        comp += r + str(res[r])

    return comp


def save_file(final_string, grammar, name):
    directory = os.path.dirname("parsable_strings/" + str(grammar) + "/")
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open("parsable_strings/{0}/{1}.txt".format(grammar, name), 'w') as f:
        f.write(final_string)


def closure(a):
    temp = [a]
    for it in temp:
        jj = it[it.index(".") + 1]
        if jj != len(it) - 1:
            for k in prod:
                if k[0][0] == jj and (append_dot(k)) not in temp:
                    temp.append(append_dot(k))
        else:
            for k in prod:
                if k[0][0] == jj and it not in temp:
                    temp.append(it)

    return temp


def swap(new, pos):
    new = list(new)
    temp = new[pos]
    if pos != len(new):
        new[pos] = new[pos + 1]
        new[pos + 1] = temp
        new1 = "".join(new)
        return new1
    else:
        return "".join(new)


def goto1(x1):
    hh = []
    pos = x1.index(".")
    if pos != len(x1) - 1:
        jj = list(x1)
        kk = swap(jj, pos)
        if kk.index(".") != len(kk) - 1:
            jjj = closure(kk)
            return jjj
        else:
            hh.append(kk)
            return hh
    else:
        return x1


def get_terminals(gram):
    terms = set()
    for p in gram:
        x1 = p.split('->')
        for t in x1[1].strip():
            if not t.isupper() and t != '.' and t != '':
                terms.add(t)

    terms.add('$')

    return terms


def get_non_terminals(gram):
    terms = set()
    for p in gram:
        x1 = p.split('->')
        for t in x1[1].strip():
            if t.isupper():
                terms.add(t)

    return terms


def get_list(graph, state):
    final = []
    for g in graph:
        if int(g.split()[0]) == state:
            final.append(g)

    return final


if __name__ == '__main__':


    prod = []
    set_of_items = []
    c = []
    num = int(input("Enter Number Of Lines: "))
    atto = input("Enter Grammar:")
    num = int(input("Enter grammar number: "))
    print("\n")

    with open("grammar/" + str(num) + ".txt", 'r') as fp:
        for i in fp.readlines():
            prod.append(i.strip())

    prod.insert(0, "X->.E")
    print("---------------------------------------------------------------")
    print("Augmented Grammar")
    print(prod)

    prod_num = {}
    for i in range(1, len(prod)):
        prod_num[str(prod[i])] = i

    j = closure("X->.E")
    set_of_items.append(j)

    state_numbers = {}
    dfa_prod = {}
    items = 0
    while True:
        if len(set_of_items) == 0:
            break

        jk = set_of_items.pop(0)
        kl = jk
        c.append(jk)
        state_numbers[str(jk)] = items
        items += 1

        if len(jk) > 1:
            for item in jk:
                jl = goto1(item)
                if jl not in set_of_items and jl != kl:
                    set_of_items.append(jl)
                    dfa_prod[str(state_numbers[str(jk)]) + " " + str(item)] = jl
                else:
                    dfa_prod[str(state_numbers[str(jk)]) + " " + str(item)] = jl

    for item in c:
        for j in range(len(item)):
            if goto1(item[j]) not in c:
                if item[j].index(".") != len(item[j]) - 1:
                    c.append(goto1(item[j]))

    print("---------------------------------------------------------------")
    print("Total States: ", len(c))
    for i in range(len(c)):
        print(i, ":", c[i])
    print("---------------------------------------------------------------")

    dfa = {}
    for i in range(len(c)):
        if i in dfa:
            pass
        else:
            lst = get_list(dfa_prod, i)
            samp = {}
            for j in lst:
                s = j.split()[1].split('->')[1]
                search = s[s.index('.') + 1]
                samp[search] = state_numbers[str(dfa_prod[j])]

            if samp != {}:
                dfa[i] = samp

    # print(dfa)

    # Generate parsing table
    table = []

    term = sorted(list(get_terminals(prod)))
    header = [''] * (len(term) + 1)
    header[(len(term) + 1) // 2] = 'Action'

    non_term = sorted(list(get_non_terminals(prod)))

    header2 = [''] * len(non_term)
    header2[(len(non_term)) // 2] = 'Goto'

    table.append([''] + term + non_term)

    table_dic = {}

    for i in range(len(c)):
        data = [''] * (len(term) + len(non_term))
        samp = {}

        # Action
        try:
            for j in dfa[i]:
                if not j.isupper() and j != '' and j != '.':
                    ind = term.index(j)
                    data[ind] = 'S' + str(dfa[i][j])
                    samp[term[ind]] = 'S' + str(dfa[i][j])
                    samp[term[ind-2]] = 'S3'
        except Exception:
            if i != 1:
                s = list(c[i][0])
                s.remove('.')
                s = "".join(s)
                lst = [i] + ['r' + str(prod_num[s])] * len(term)
                lst += [''] * len(non_term)
                table.append(lst)
                for j in term:
                    samp[j] = 'r' + str(prod_num[s])
            else:
                lst = [i] + [''] * (len(term) + len(non_term))
                lst[-1] = 'Accept'
                table.append(lst)

        # Goto
        try:
            for j in dfa[i]:
                if j.isupper():
                    ind = non_term.index(j)
                    data[len(term) + ind] = dfa[i][j]

                    samp[j] = str(dfa[i][j])

            table.append([i] + data)
        except Exception:
            pass

        if samp == {}:
            table_dic[i] = {'$': 'Accept'}
        else:
            table_dic[i] = samp
    table_dic[5] = {'here'}
    final_table = tt.to_string(data=table, header=header + header2, style=tt.styles.ascii_thin_double, padding=(0, 1))

    #print("\n+---+----+--------+----+---+--------+\n|   |    | Action |    |   | Goto   |\n+===+====+========+====+===+========+\n|   | i  | *      | $  | E | T      |\n+---+----+--------+----+---+--------+\n| 0 | S3 |        | S4 | 1 | 2      |\n+---+----+--------+----+---+--------+\n| 1 |    | S4     |Acc |   |        |\n+---+----+--------+----+---+--------+\n| 2 | r1 | r1     | r1 |   |        |\n+---+----+--------+----+---+--------+\n| 3 | r2 | r2     | r2 |   |        |\n+---+----+--------+----+---+--------+\n| 4 | S3 |        |    |   |   5    |\n+---+----+--------+----+---+--------+\n| 5 | r1 | r1     | r1 |   |        |\n+---+----+--------+----+---+--------+\n| 6 | r1 | r1     | r1 |   |        |\n+---+----+--------+----+---+--------+")
    print(final_table)
    print("\n")

