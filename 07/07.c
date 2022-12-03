#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <limits.h>

typedef long long ll;
typedef ll (*dist)(const ll, const ll);

ll d1(const ll a, const ll b) { return llabs(a-b); }
ll d2(const ll a, const ll b) { return llabs(a-b) * (llabs(a-b)+1) / 2; }

ll minimize(const ll *const nums, const int len, const dist d) {
  ll best = LLONG_MAX, min = LLONG_MAX, max = LLONG_MIN;

  for (int i = 0; i < len; ++i) {
    if (nums[i] < min) min = nums[i];
    if (nums[i] > max) max = nums[i];
  }

  for (ll n = min; n <= max; ++n) {
    ll s = 0;
    for (int j = 0; j < len; ++j) s += d(n, nums[j]);
    if (s < best) best = s;
  }

  return best;
}

int main() {

  int cap = 128, len = 0;
  ll n, *nums = malloc(sizeof(ll) * cap);
  while (scanf("%lld", &n) != EOF) {
    if (len == cap) {
      nums = memcpy(malloc(sizeof(ll) * (cap<<1)), nums, sizeof(ll)*cap);
      cap <<= 1;
    }
    nums[len++] = n;
    scanf(",");
  }

  printf("%lld %lld\n", minimize(nums, len, d1), minimize(nums, len, d2));

  free(nums);
  return 0;
}
