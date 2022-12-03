#include "string.h"
#include "stdio.h"

typedef long long ctr_t[256*256];
typedef char rules_t[256*256];

typedef struct{
  ctr_t ctr;
  rules_t rules;
  char last;
} input_t;

int hash(char a, char b) {
  return a*256+b;
}

long long solve(const input_t *const input, const int times) {
  ctr_t ctr = {};
  memcpy(ctr, input->ctr, 256*256*sizeof(long long));

  for (int i = 0; i < times; ++i) {
    ctr_t new_ctr = {};
    for (char a = 'A'; a <= 'Z'; ++a) for (char b = 'A'; b <= 'Z'; ++b) {
      int h = hash(a, b);
      long long n = ctr[h];
      if (input->rules[h] == 0) new_ctr[h] += n;
      else {
        char c = input->rules[h];
        new_ctr[hash(a, c)] += n;
        new_ctr[hash(c, b)] += n;
      }
    }
    memcpy(ctr, new_ctr, 256*256*sizeof(long long));
  }

  long long letters[256] = {};
  for (char a = 'A'; a <= 'Z'; ++a) for (char b = 'A'; b <= 'Z'; ++b)
    letters[a] += ctr[hash(a, b)];
  ++letters[input->last];

  long long high = 0, low = 0;
  for (int a = 'A'; a <= 'Z'; ++a) {
    long long n = letters[a];
    if (!n) continue;
    if (n > high) high = n;
    if (!low || n < low) low = n;
  }

  return high-low;
}

int main() {
  input_t input = {};

  char prev = 0;
  for (;;) {
    char c[2];
    scanf("%1[A-Z\n]", c);
    if (*c == '\n') break;
    if (input.last) ++input.ctr[hash(input.last, *c)];
    input.last = *c;
  }

  for (;;) {
    char a, b, c;
    if (scanf(" %c%c -> %c", &a, &b, &c) == EOF) break;
    input.rules[hash(a, b)] = c;
  }

  printf("%lld %lld\n", solve(&input, 10), solve(&input, 40));
}
