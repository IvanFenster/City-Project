graph = [[] for _ in range(82)]
usable_vert = [i for i in range(10, 72)]
usable_vert += [1, 9, 72, 80]
goal_for_taxi = usable_vert.copy()
for i in [1, 9, 72, 80, 63, 45, 27, 17, 15, 13, 11, 18, 36, 34, 64, 66, 68, 70]:
    goal_for_taxi.remove(i)
print(goal_for_taxi)
