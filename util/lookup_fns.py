from .definitions import substat
mu_cache = {
    (8, 1): 3/4,
    (9, 1): 2/4,
    (10, 1): 1/4,
    (15, 2): 15/16,
    (16, 2): 13/16,
    (17, 2): 10/16,
    (18, 2): 6/16,
    (19, 2): 3/16,
    (20, 2): 1/16,
    (22, 3): 63/64,
    (23, 3): 60/64,
    (24, 3): 54/64,
    (25, 3): 44/64,
    (26, 3): 32/64,
    (27, 3): 20/64,
    (28, 3): 10/64,
    (29, 3): 4/64,
    (30, 3): 1/64,
    (29, 4): 255/256,
    (30, 4): 251/256,
    (31, 4): 241/256,
    (32, 4): 221/256,
    (33, 4): 190/256,
    (34, 4): 150/256,
    (35, 4): 106/256,
    (36, 4): 66/256,
    (37, 4): 35/256,
    (38, 4): 15/256,
    (39, 4): 5/256,
    (40, 4): 1/256,
    (36, 5): 1023/1024,
    (37, 5): 1018/1024,
    (38, 5): 1003/1024,
    (39, 5): 968/1024,
    (40, 5): 903/1024,
    (41, 5): 802/1024,
    (42, 5): 667/1024,
    (43, 5): 512/1024,
    (44, 5): 357/1024,
    (45, 5): 222/1024,
    (46, 5): 121/1024,
    (47, 5): 56/1024,
    (48, 5): 21/1024,
    (49, 5): 6/1024,
    (50, 5): 1/1024,
    (43, 6): 4095/4096,
    (44, 6): 4089/4096,
    (45, 6): 4068/4096,
    (46, 6): 4012/4096,
    (47, 6): 3892/4096,
    (48, 6): 3676/4096,
    (49, 6): 3340/4096,
    (50, 6): 2884/4096,
    (51, 6): 2338/4096,
    (52, 6): 1758/4096,
    (53, 6): 1212/4096,
    (54, 6): 756/4096,
    (55, 6): 420/4096,
    (56, 6): 204/4096,
    (57, 6): 84/4096,
    (58, 6): 28/4096,
    (59, 6): 7/4096,
    (60, 6): 1/4096,
}
sig_cache = {
    ((0,), 1): 3/4,
    ((1,), 1): 1/4,
    ((0,), 2): 9/16,
    ((1,), 2): 6/16,
    ((2,), 2): 1/16,
    ((0,), 3): 27/64,
    ((1,), 3): 27/64,
    ((2,), 3): 9/64,
    ((3,), 3): 1/64,
    ((0,), 4): 81/256,
    ((1,), 4): 108/256,
    ((2,), 4): 54/256,
    ((3,), 4): 12/256,
    ((4,), 4): 1/256,
    ((0,), 5): 243/1024,
    ((1,), 5): 405/1024,
    ((2,), 5): 270/1024,
    ((3,), 5): 90/1024,
    ((4,), 5): 15/1024,
    ((5,), 5): 1/1024,
    ((0, 0), 1): 2/4,
    ((0, 1), 1): 1/4,
    ((0, 0), 2): 4/16,
    ((0, 1), 2): 4/16,
    ((0, 2), 2): 1/16,
    ((1, 1), 2): 2/16,
    ((0, 0), 3): 8/64,
    ((0, 1), 3): 12/64,
    ((0, 2), 3): 6/64,
    ((0, 3), 3): 1/64,
    ((1, 1), 3): 12/64,
    ((1, 2), 3): 3/64,
    ((0, 0), 4): 16/256,
    ((0, 1), 4): 32/256,
    ((0, 2), 4): 24/256,
    ((0, 3), 4): 8/256,
    ((0, 4), 4): 1/256,
    ((1, 1), 4): 48/256,
    ((1, 2), 4): 24/256,
    ((1, 3), 4): 4/256,
    ((2, 2), 4): 6/256,
    ((0, 0), 5): 32/1024,
    ((0, 1), 5): 80/1024,
    ((0, 2), 5): 80/1024,
    ((0, 3), 5): 40/1024,
    ((0, 4), 5): 10/1024,
    ((0, 5), 5): 1/1024,
    ((1, 1), 5): 160/1024,
    ((1, 2), 5): 120/1024,
    ((1, 3), 5): 40/1024,
    ((1, 4), 5): 5/1024,
    ((2, 2), 5): 60/1024,
    ((2, 3), 5): 10/1024,
    ((0, 0, 0, 1), 1): 1/4,
    ((0, 0, 0, 2), 2): 1/16,
    ((0, 0, 1, 1), 2): 2/16,
    ((0, 0, 0, 3), 3): 1/64,
    ((0, 0, 1, 2), 3): 3/64,
    ((0, 1, 1, 1), 3): 6/64,
    ((0, 0, 0, 4), 4): 1/256,
    ((0, 0, 1, 3), 4): 4/256,
    ((0, 0, 2, 2), 4): 6/256,
    ((0, 1, 1, 2), 4): 12/256,
    ((1, 1, 1, 1), 4): 24/256,
    ((0, 0, 0, 5), 5): 1/1024,
    ((0, 0, 1, 4), 5): 5/1024,
    ((0, 0, 2, 3), 5): 10/1024,
    ((0, 1, 1, 3), 5): 20/1024,
    ((0, 1, 2, 2), 5): 30/1024,
    ((1, 1, 1, 2), 5): 60/1024,
}
prob_subs_summary = {
    0: {(4, 6, 6, 6): 31833 / 2351440, (3, 6, 6, 6): 35150679 / 3618174560,
        (4, 4, 6, 6): 12247 / 1492260, (3, 4, 6, 6): 6395431221 / 1085396703776, (3, 3, 6, 6): 588789 / 139160560,
        (4, 4, 4, 6): 4249 / 852720, (3, 4, 4, 6): 83731933 / 23392170340, (3, 3, 4, 6): 53217 / 20691880,
        (4, 4, 4, 4): 1 / 330, (3, 4, 4, 4): 17447 / 8009760, (3, 3, 4, 4): 50647 / 32339406, },
    6: {(4, 4, 6, 6): 222877 / 12932920, (3, 4, 6, 6): 1724981913 / 140744203600,  (3, 3, 6, 6): 80433 / 9225944,
        (4, 4, 4, 6): 2407 / 235144, (3, 4, 4, 6): 15233623 / 2090714400, (3, 3, 4, 6): 3427272 / 660607675,
        (4, 4, 4, 4): 128 / 20995, (3, 4, 4, 4): 35624 / 8200647, (3, 3, 4, 4): 7813 / 2523276, },
    4: {(4, 6, 6, 6): 29 / 1309, (3, 6, 6, 6): 4745547 / 300284600,
        (4, 4, 6, 6): 1475 / 111384, (3, 4, 6, 6): 1824571 / 193040100, (3, 3, 6, 6): 92097 / 13649300,
        (4, 4, 4, 6): 589 / 74256, (3, 4, 4, 6): 1979168149 / 349325364960, (3, 3, 4, 6): 16088 / 3974355,
        (4, 4, 4, 4): 1 / 210, (3, 4, 4, 4): 27001 / 7931616, (3, 3, 4, 4): 70339 / 28893744, },
    3: {(4, 6, 6, 6): 106873344 / 5489226575, (3, 6, 6, 6): 5262165 / 378263704,
        (4, 4, 6, 6): 39435776 / 3375362925, (3, 4, 6, 6): 66962957661 / 8017134743800,
        (4, 4, 4, 6): 33193984 / 4725508095, (3, 4, 4, 6): 151137649 / 30075647580,
        (4, 4, 4, 4): 2048 / 483923, (3, 4, 4, 4): 2368048 / 781535645, }
}

def mu_sanity(a, n):
    if a <= 7*n:
        return 1
    elif a > 10*n:
        return 0
    return mu_cache[(a, n)]

def sigma_sanity(ss, n):
    if len(ss) > 4 or sum(ss) > n: return 0
    if len(ss) == 4 and sum(ss) != n: return 0
    if len(ss) == 3:
        ss = [*ss, n-sum(ss)]
    ss = tuple(sorted(ss))
    return sig_cache[(ss, n)]


mu_arr = [1023/1024, 1018/1024, 1003/1024, 968/1024, 903/1024, 802/1024, 667/1024, 512/1024, 357/1024, 222/1024, 121/1024, 56/1024, 21/1024, 6/1024, 1/1024, 4095/4096, 4089/4096, 4068/4096, 4012/4096, 3892/4096, 3676/4096, 3340/4096, 2884/4096, 2338/4096, 1758/4096, 1212/4096, 756/4096, 420/4096, 204/4096, 84/4096, 63/64, 60/64, 54/64, 44/64, 32/64, 20/64, 10/64, 4/64, 1/64, 150/256, 106/256, 66/256, 35/256, 15/256, 5/256, 1/256, 15/16, 13/16, 10/16, 6/16, 3/16, 255/256, 251/256, 241/256, 221/256, 190/256, 3/4, 2/4, 1/4, 28/4096, 7/4096, 1/4096, 1/16]
sig_arr = [270/1024, 80/1024, 0, 12/256, 8/256, 120/1024, 0, 60/1024, 4/256, 60/1024, 4/256, 30/1024, 24/256, 160/1024, 1/64, 1/64, 24/256, 1/64, 12/256, 0, 6/256, 2/16, 6/256, 0, 81/256, 16/256, 0, 27/64, 12/64, 0, 1/16, 1/16, 12/64, 1/16, 6/64, 3/4, 2/4, 243/1024, 32/1024, 0, 108/256, 32/256, 0, 9/64, 6/64, 48/256, 0, 24/256, 3/64, 5/1024, 3/64, 5/1024, 0, 405/1024, 80/1024, 0, 54/256, 90/1024, 40/1024, 0, 1/256, 1/256, 40/1024, 1/256, 20/1024, 9/16, 4/16, 0, 1/4, 1/4, 0, 1/4, 27/64, 8/64, 0, 6/16, 4/16, 10/1024, 0, 10/1024, 2/16, 0, 0, 0, 15/1024, 10/1024, 1/1024, 1/1024, 0, 1/1024]

mur = (56, 41, 62, 30, 46, 39, 0, 10, 20, 59)
def mu(a, n):
    if a <= 7*n: return 1
    elif a > 10*n: return 0

    # offset = -16
    # t = 10
    v = a + 8*n - 16
    x = v % 10
    y = v // 10
    return mu_arr[x + mur[y]]

sigr = (35, 64, 70, 21, 33, 45, 12, 0, 53, 76, 48, 86)
def sigma(ss, n):
    if len(ss) > 4 or sum(ss) > n: return 0
    if len(ss) == 4 and sum(ss) != n: return 0
    if len(ss) == 3: ss = [*ss, n-sum(ss)]
    ss = sorted(ss)

    # t = 12
    # offset = -14
    v = 13*n + len(ss) - 14 + 16*ss[-1]  # max(ss)
    if len(ss) > 1: v += 4*ss[-2]
    x = v % 12
    y = v // 12
    return sig_arr[x + sigr[y]]

def p_subs(vs, main_type):
    srch_key = tuple(sorted(map(lambda s: substat.distr[s], vs)))
    if main_type not in substat.distr:
        return prob_subs_summary[0][srch_key]
    return prob_subs_summary[substat.distr[main_type]][srch_key]

if __name__ == '__main__':
    import itertools
    for rep in range(1,6):
        for ks in itertools.product(range(10), repeat=rep):
            for n in range(1,6):
                if sigma_sanity(ks,n) != sigma(ks,n):
                    print(f'Failed at {ks}, {n}')

    for a in range(80):
        for n in range(6):
            if mu_sanity(a, n) != mu(a, n):
                print(f'Failed mu at ({a}, {n})')
    exit(0)