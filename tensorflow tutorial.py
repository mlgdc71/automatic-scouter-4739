import torch as t

d = "cuda" if t.cuda.is_available() else "cpu"

my_tensor = t.tensor([1, 2, 3], [4,5,6], [7,8,9], dtype=t.float64, device=d,
                     )

print(my_tensor)
