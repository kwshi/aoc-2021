pairs = Dict{Char, Char}('{' => '}', '(' => ')', '[' => ']', '<' => '>')
penalty = Dict{Char, Int}(')' => 3, ']' => 57, '}' => 1197, '>' => 25137)
value = Dict{Char, Int}(')' => 1, ']' => 2, '}' => 3, '>' => 4)

function parse(line::String)
  stack::Vector{Char} = []
  for c ∈ line
    if c ∈ keys(pairs)
      push!(stack, pairs[c])
      continue
    end
    if c ≠ pop!(stack)
      return penalty[c], stack
    end
  end
  return 0, stack
end

complete(stack::Vector{Char}) = foldr(stack; init=0) do c, total
  total * 5 + value[c]
end

function main(lines::Base.EachLine)
  parsed = map(parse, lines) |> collect

  p1 = sum(map(first, parsed))
  p2 = sum(complete(stack) for (p, stack) in parsed if p == 0)

  (p1, p2)
end

main(eachline()) |> println
