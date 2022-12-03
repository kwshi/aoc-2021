using DataStructures

nums = counter(parse(Int64, s) for s in split(readline(), ","))

d1(a, b) = abs(a-b)
d2(a, b) = abs(a-b) * (abs(a-b)+1) ÷ 2

minimize(d) = minimum(
  sum(ct * d(n, m) for (m, ct) in nums)
  for n in minimum(keys(nums)):maximum(keys(nums))
)

println((minimize(d1), minimize(d2)))
