#include <bits/stdc++.h>

struct State {
  int w, x, y, z;
};

bool operator==(const State& a, const State& b) {
  return a.w == b.w && a.x == b.x && a.y == b.y && a.z == b.z;
}

template<> struct std::hash<State> {
  size_t operator()(const State& state) const noexcept {
    return ((state.w * 37 + state.x) * 37 + state.y) * 37 + state.z;
  }
};

using States = std::unordered_map<State, long long>;

int main() {
  States states;
  states.emplace(State{0, 0, 0, 0}, 0);

  for (;;) {
    char instr[4];
    if (scanf(" %2s", instr) == EOF) break;
    if (strcmp(instr, "inp") == 0) {
    } else if (strcmp(instr, "add") == 0) {
    } else if (strcmp(instr, "mul") == 0) {
    } else if (strcmp(instr, "mod") == 0) {
    } else if (strcmp(instr, "div") == 0) {
    } else if (strcmp(instr, "eql") == 0) {
    }
    printf("%s\n", instr);
  }

}
