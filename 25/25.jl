using Base.Iterators

function step(grid::Matrix{Char}, key::Char, di::Int, dj::Int)
  h, w = size(grid)
  new = [ '.' for _ ∈ 1:h, _ ∈ 1:w ]
  for (p, c) ∈ pairs(grid)
    i′ = mod((p[1]+di-1), h) + 1
    j′ = mod((p[2]+dj-1), w) + 1

    if c == '.' continue end

    if c == key && grid[i′, j′] == '.'
      new[i′, j′] = c
    else
      new[p] = c
    end
  end
  new
end

function evolve(grid::Matrix{Char})
  step(step(grid, '>', 0, 1), 'v', 1, 0)
end

function main()
  grid = vcat(map(permutedims ∘ collect, readlines())...)
  for i in countfrom()
    new = evolve(grid)
    if new == grid
      println(i)
      return
    end
    grid = new
  end

end

main()
