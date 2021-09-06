from random import shuffle


def hashtag_list_to_follow_per_hashtag_list(hashtag_list, follow_amount):
    res = []
    t = hashtag_list
    t_temp = t

    if follow_amount == 0:
        for _ in hashtag_list:
            res.append(0)
        return res

    if follow_amount < len(t):
        t_temp = t[:follow_amount]

    if len(t) > 1:
        if len(t_temp) % 2 != 0:
            use_len = len(t_temp) - 1
            res.append(1)
        else:
            use_len = len(t_temp)

        for _ in range(use_len):
            res.append(follow_amount // use_len)
        for _ in range(len(t) - len(t_temp)):
            res.append(0)

        if sum(res) != follow_amount:
            res[0] += 1

    else:
        res = [follow_amount]
    shuffle(res)
    a2g = lambda x: (n for n in x)
    return a2g(res)
