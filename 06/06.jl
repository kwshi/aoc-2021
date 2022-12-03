import DataStructures as DS
import Printf

function sim(f, n)
  fish = copy(f)

  for _ in 1:n
    new = fish[0]
    for i in 0:8
      fish[i] = fish[i+1]
    end
    fish[6] += new
    fish[8] = new
  end

  sum(values(fish))
end

function main()
  fish = DS.counter(parse(Int, s) for s in split(readline(), ","))

  @Printf.printf "%d %d\n" sim(fish, 80) sim(fish, 256)
end

main()
