with open("one.txt", "r") as f:
    d = {}

    st = f.read()

    for i in range(0, len(st) - 3, 3):
        tri = st[i:i+3]
        d[tri] = d.get(tri, 0) + 1

    print({k: v for k, v in sorted(d.items(), key=lambda item: item[1])})

