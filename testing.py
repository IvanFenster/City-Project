import random
graph = [[10, 18], [], [], [], [], [], [], [], [17, 26], [], [20, 12], [18, 1], [22, 14], [20, 11], [24, 16], [22, 13], [26, 9], [24, 15], [36, 28], [10, 1], [38, 29, 30], [11, 12], [40, 31, 32], [13, 14], [42, 33, 34], [15, 16], [44, 35], [17, 9], [38, 21, 30], [36, 19], [40, 23, 32], [38, 21, 29], [42, 25, 34], [40, 23, 31], [44, 27], [42, 25, 33], [54, 46], [19, 28], [56, 47, 48], [21, 29, 30], [58, 49, 50], [23, 31, 32], [60, 51, 52], [25, 33, 34], [62, 53], [27, 35], [56, 39, 48], [54, 37], [58, 41, 50], [56, 39, 47], [60, 43, 52], [58, 41, 49], [62, 45], [60, 43, 51], [64, 72], [37, 46], [65, 66], [39, 47, 48], [67, 68], [41, 49, 50], [69, 70], [43, 51, 52], [71, 80], [45, 53], [57, 66], [55, 72], [59, 68], [57, 65], [61, 70], [59, 67], [63, 80], [61, 69], [], [55, 64], [], [], [], [], [], [], [], [63, 71]]
usable_vert = [i for i in range(10, 72)]
usable_vert += [1, 9, 72, 80]

def new_path(now):
    queue = []
    color = [0 for _ in range(82)]
    dist = [0 for _ in range(82)]
    prev = [-2 for _ in range(82)]
    cur_vert = now
    goal = random.choice(usable_vert)
    queue.append(cur_vert)
    color[cur_vert] = 1

    while len(queue) > 0:
        v = queue[0]
        queue.pop(0)
        for u in graph[v]:
            if color[u] == 0:
                color[u] = 1
                dist[u] = dist[v] + 1
                prev[u] = v
                queue.append(u)

    dist_to_goal = dist[goal]
    pr = prev[goal]
    path = []
    while pr != now:
        path.append(pr)
        pr = prev[pr]
    path.reverse()
    path.append(goal)
    for i in path:
        if i < 0:
            print('!!ALERT!! NUM: 2')
            print('path:', path)
            print('goal:', goal)
            print('prev:', prev)
    return goal, path

print(new_path(34))