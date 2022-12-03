#include <stdio.h>
#include <stdlib.h>
#include <string.h>

long long simulate(const long long f[9], const int turns) {
  long long fish[9];
  memcpy(fish, f, sizeof(fish));

  for (int i = 0; i < turns; ++i) {
    long long new = fish[0];
    for (int j = 0; j < 8; ++j) fish[j] = fish[j+1];
    fish[6] += new;
    fish[8] = new;
  }

  long long total = 0;
  for (int i = 0; i < 9; ++i) total += fish[i];
  return total;
}

int main() {
  long long fish[9] = {};

  char buf[4096];
  fgets(buf, 4096, stdin);
  buf[4095] = '\0';

  for (char *s = strtok(buf, ","); s != NULL; s = strtok(NULL, ",")) {
    int n = atoi(s);
    ++fish[n];
  }

  printf("%lld %lld\n", simulate(fish, 80), simulate(fish, 256));

  return 0;
}
