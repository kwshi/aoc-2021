#include <bits/stdc++.h>

std::array<int, 4> costs{1, 10, 100, 1000};

constexpr int depth{4};

using Node = std::pair<int, std::string>;
using Frontier = std::priority_queue<Node, std::vector<Node>, std::greater<Node>>;

void pprint(const std::string& state) {
  std::cout
    << "  #############\n"
    << "  #" << state.substr(0, 11) << "#\n";
  for (int j{}; j < depth; ++j) {
    std::cout << (j==0 ? "  ###" : "    #");
    for (int i{}; i < 4; ++i)
      std::cout << state[11+i*depth+(depth-1-j)] << '#';
    std::cout << (j==0 ? "##\n" : "\n");
  }
  std::cout << "    #########" << std::endl;
}

void explore_out(const std::string& state, const int room, const int level, const int dist, const int dir, Frontier& frontier) {
  const int k{11+depth*room+level};
  const int cost{costs[state[k]-'A']};
  const int x{2*(room+1)};

  for (int d{1}; 0 <= x+dir*d && x+dir*d < 11 && state[x+dir*d] == '.'; ++d) {
    const int xx{x+dir*d};
    if (xx%2==0 && 2<=xx && xx<=8) continue; // stopping directly above a room
    std::string next{state};
    next[k] = '.';
    next[xx] = state[k];
    frontier.emplace(dist + (depth-level+d)*cost, next);
  }
}

void explore_in(const std::string& state, const int room, const int level, const int dist, const int dir, Frontier& frontier) {
  const int k{11+depth*room+level};
  //const int cost{costs[state[k]-'A']};
  const int x{2*(room+1)};

  for (int d{1}; 0 <= x+dir*d && x+dir*d < 11; ++d) {
    const int xx{x+dir*d};
    if (state[xx] == '.') continue;
    if (state[xx]-'A' != room) break;
    int cost{costs[room]};
    std::string next{state};
    next[xx] = '.';
    next[k] = state[xx];
    frontier.emplace(dist + (depth-level+d)*cost, next);
  }
}

int main() {

  std::string optimal(11+depth*4, '.');
  for (int i{}; i < 4; ++i)
    for (int j{}; j < depth; ++j)
      optimal[11+depth*i+j] = 'A'+i;

  //std::string start{"...........ABDCCBAD"};
  //std::string start{"...........CDABADCB"};
  std::string start{"...........CDDDABCBAABDCCAB"};
  //std::string start{"...........ADDBDBCCCABBACAD"};

  Frontier frontier;
  frontier.emplace(0, start);

  std::unordered_map<std::string, int> done;

  while (!frontier.empty()) {

    const auto parent{frontier.top()};
    frontier.pop();

    const auto& state{parent.second};

    if (done.contains(state)) continue;
    done[state] = parent.first;

    std::cout << "parent " << parent.first << "\n";
    pprint(state);
    if (state == optimal) {
      std::cout << "perfect!!\n" << parent.first << std::endl;
      break;
    }

    for (int i{}; i < 4; ++i) {
      const int x{2*(i+1)};
      const int bot{11+2*i};
      const int top{12+2*i};

      // move out of room i, level j only if:
      // - possible--j is nonempty, and above j is empty
      // - necessary--j or below are in non-home room

      // move into room i, level j only if
      // - possible--j and above are empty
      // - acceptable--all below j are home, and move target is home

      // in fact, at most one move-out/in per column is possible, so find top
      // element and check that there is reason to move (out: it or below is
      // different; in: everything below + move-in target is good).

      int j{};
      bool settled{true};

      for (; j < depth && state[11+depth*i+j] != '.'; ++j)
        settled &= state[11+depth*i+j] - 'A' == i;

      if (!settled && j) {
        // j-1 moves out; try all spots
        explore_out(state, i, j-1, parent.first, 1, frontier);
        explore_out(state, i, j-1, parent.first, -1, frontier);
      }

      if (settled && j < depth) {
        // move into j
        explore_in(state, i, j, parent.first, 1, frontier);
        explore_in(state, i, j, parent.first, -1, frontier);
      }
    }
  }
}
