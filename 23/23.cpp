#include <bits/stdc++.h>

std::array<int, 4> costs{1, 10, 100, 1000};

using Node = std::pair<int, std::string>;

bool perfect(const std::string& state) {
  return state == "...........AABBCCDD";
}

void pprint(const std::string& state) {
  std::cout
    << "  #############\n"
    << "  #" << state.substr(0, 11) << "#\n  ###";
  for (int i{}; i < 4; ++i)
    std::cout << state[12+2*i] << '#';
  std::cout << "##\n    #";
  for (int i{}; i < 4; ++i)
    std::cout << state[11+2*i] << '#';
  std::cout << "\n    #########" << std::endl;
}

int main() {

  //std::string start{"...........ABDCCBAD"};
  std::string start{"...........CDABADCB"};

  std::priority_queue<Node, std::vector<Node>, std::greater<Node>> frontier;
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
    if (perfect(state)) {
      std::cout << "perfect!!\n" << parent.first << std::endl;
      break;
    }

    for (int i{}; i < 4; ++i) {
      const int x{2*(i+1)};
      const int bot{11+2*i};
      const int top{12+2*i};

      // move out; only do so if possible and necessary
      if (state[top] != '.' && (state[bot]-'A' != i || state[top]-'A' != i)) {
        const int cost{costs[state[top]-'A']};

        // top move out if either in stack is different from home
        for (int d{1}; x+d < 11 && state[x+d] == '.'; ++d) {
          const int xx{x+d};
          if (xx%2==0 && 2<=xx && xx<=8) continue;
          std::string next{state};
          next[top] = '.';
          next[xx] = state[top];
          frontier.emplace(parent.first + (d+1)*cost, next);
          std::cout << "child top out right\n";
          pprint(next);
        }

        // left
        for (int d{1}; x-d >= 0 && state[x-d] == '.'; ++d) {
          const int xx{x-d};
          if (xx%2==0 && 2<=xx & xx<=8) continue;
          std::string next{state};
          next[top] = '.';
          next[xx] = state[top];
          frontier.emplace(parent.first + (d+1)*cost, next);
          std::cout << "child top out left\n";
          pprint(next);
        }
      }

      if (state[bot] != '.' && (state[bot]-'A' != i && state[top]=='.')) {
        // bottom move out if top is free and bottom not home

        const int cost{costs[state[bot]-'A']};

        for (int d{1}; x+d < 11 && state[x+d] == '.'; ++d) {
          const int xx{x+d};
          if (xx%2==0 && 2<=xx && xx<=8) continue;
          std::string next{state};
          next[bot] = '.';
          next[xx] = state[bot];
          frontier.emplace(parent.first + (d+2)*cost, next);

          std::cout << "child bot out right\n";
          pprint(next);
        }

        for (int d{1}; x-d >= 0 && state[x-d] == '.'; ++d) {
          const int xx{x-d};
          if (xx%2==0 && 2<=xx && xx<=8) continue;
          std::string next{state};
          next[bot] = '.';
          next[xx] = state[bot];
          frontier.emplace(parent.first + (d+2)*cost, next);

          std::cout << "child bot out left\n";
          pprint(next);
        }

      }

      // move in; only do so if finalizable and possible
      if (state[bot]-'A' == i && state[top] == '.') {
        // move to top only if available, and bottom already good

        int cost{costs[i]};

        for (int d{1}; x+d < 11; ++d) {
          const int xx{x+d};
          if (xx%2==0 && 2<=xx && xx<=8 || state[xx]=='.') continue;
          if (state[xx]-'A' != i) break;
          auto next{state};
          next[xx] = '.';
          next[top] = state[xx];
          frontier.emplace(parent.first + (d+1)*cost, next);

          std::cout << "child top in right\n";
          pprint(next);
          break;
        }

        for (int d{1}; x-d >= 0; ++d) {
          const int xx{x-d};
          if (xx%2==0 && 2<=xx && xx<=8 || state[xx]=='.') continue;
          if (state[xx]-'A' != i) break;
          auto next{state};
          next[xx] = '.';
          next[top] = state[xx];
          frontier.emplace(parent.first + (d+1)*cost, next);

          std::cout << "child top in left\n";
          pprint(next);
          break;
        }

      }
      if (state[bot] == '.' && state[top] == '.') {
        // move to bottom only if empty

        int cost{costs[i]};

        for (int d{1}; x+d < 11; ++d) {
          const int xx{x+d};
          if (xx%2 == 0 && 2<=xx && xx<=8 || state[xx]=='.') continue;
          if (state[xx]-'A' != i) break;
          auto next{state};
          next[xx] = '.';
          next[bot] = state[xx];
          frontier.emplace(parent.first + (d+2)*cost, next);

          std::cout << "child bot in right\n";
          pprint(next);
          break;
        }

        for (int d{1}; x-d >= 0; ++d) {
          const int xx{x-d};
          if (xx%2 == 0 && 2<=xx && xx<=8 || state[xx]=='.') continue;
          if (state[xx]-'A' != i) break;
          auto next{state};
          next[xx] = '.';
          next[bot] = state[xx];
          frontier.emplace(parent.first + (d+2)*cost, next);

          std::cout << "child bot in left\n";
          pprint(next);
          break;
        }

      }

    }

  }

}
