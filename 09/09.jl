using DataStructures

grid = [[parse(Int, c) for c in row] for row in eachline()]

Δ = [(0, 1), (0, -1), (1, 0), (-1, 0)]

islow(i, j) = all(Δ) do δ
  i′, j′ = (i, j) .+ δ
  (
    !(1 ≤ i′ ≤ length(grid) && 1 ≤ j′ ≤ length(grid[i]))
    || grid[i][j] < grid[i′][j′]
  )
end

p1() = sum(
  1+c
  for (i, row) in enumerate(grid)
  for (j, c) in enumerate(row)
  if islow(i, j)
)

p2() = begin
  roots = [(i, j) for (i, row) in enumerate(grid) for (j, _) in enumerate(row) if islow(i, j)]
  sizes = Dict(p => 1 for p in roots)
  basins = Dict(p => p for p in roots)

  frontier = collect(roots)
  while !isempty(frontier)
    parent = pop!(frontier)
    for δ in Δ
      i′, j′ = child = parent .+ δ
      if (
          !(1 ≤ i′ ≤ length(grid) && 1 ≤ j′ ≤ length(grid[i′]))
          || grid[i′][j′] == 9
          || child ∈ keys(basins)
      )
        continue
      end
      root = basins[child] = basins[parent]
      sizes[root] += 1
      push!(frontier, child)
    end
  end

  prod(partialsort!(collect(values(sizes)), 1:3, rev=true))
end

println((p1(), p2()))
