nums = map(s -> parse(Int, s), readlines()) |> collect
incs(n::Int) = count(zip(nums, nums[1+n:end])) do (a, b) a < b end
println((incs(1), incs(3)))
