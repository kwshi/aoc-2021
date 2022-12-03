using Combinatorics

digits = [
  (0, 1, 2, 4, 5, 6),
  (2, 5),
  (0, 2, 3, 4, 6),
  (0, 2, 3, 5, 6),
  (1, 2, 3, 5),
  (0, 1, 3, 5, 6),
  (0, 1, 3, 4, 5, 6),
  (0, 2, 5),
  (0, 1, 2, 3, 4, 5, 6),
  (0, 1, 2, 3, 5, 6),
]

decoders = Dict()
for perm in permutations("abcdefg")
  decoder = Dict(join(sort([perm[i+1] for i in d])) => n for (n, d) in zip(0:9, digits))
  decoders[keys(decoder) |> collect |> sort |> Tuple] = decoder
end

function solve(line)
  pats, sigs = split(line, " | ")
  decoder = decoders[[join(sort(collect(s))) for s in split(pats)] |> sort |> Tuple]
  [decoder[join(sort(collect(s)))] for s in split(sigs)]
end

vals = map(solve, eachline()) |> collect
p1 = count(∈([1, 4, 7, 8]), [(vals...)...])
p2 = sum(1000*a+100*b+10*c+d for (a, b, c, d) in vals)
println(p1, " ", p2)
