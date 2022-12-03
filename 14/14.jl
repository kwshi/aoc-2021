using DataStructures

template = readline()
readline()
rules = map(eachline()) do line
  result = match(r"^([A-Z]{2}) -> ([A-Z])$", line)
  result[1] => result[2]
end |> Dict

function report(counts)
  letters = counter([first(template), last(template)])
  for ((a, b), n) ∈ counts
    letters[a] += n
    letters[b] += n
  end
  low, high = extrema(values(letters))
  (high - low) ÷ 2
end

function solve(times)
  counts = counter(map(((a, b),) -> "$a$b", zip(template, template[2:end])))
  for _ in 1:times
    new = Accumulator{String, Int}()
    for (pair, n) in counts
      c = get(rules, pair, Nothing)
      if isnothing(c)
        new[pair] += n
      else
        a, b = pair
        new["$a$c"] += n
        new["$c$b"] += n
      end
    end
    counts = new
  end
  report(counts)
end

println(solve(10))
println(solve(40))
