#include <bits/stdc++.h>
using namespace std;
#define debug(fmt, ...) \
  fprintf(stderr, "[%d] " fmt "\n", __LINE__, ##__VA_ARGS__)
template <class _Tx, class _Ty>
inline void chkmin(_Tx& x, const _Ty& y) {
  x = min<common_type_t<_Tx, _Ty>>(x, y);
}
template <class _Tx, class _Ty>
inline void chkmax(_Tx& x, const _Ty& y) {
  x = max<common_type_t<_Tx, _Ty>>(x, y);
}
using ll = long long;
using ull = unsigned long long;
using i128 = __int128_t;
using u128 = __uint128_t;
bool Mbe;

bool Med;
int main() {
  // debug("Mem: %.4lfMB.", fabs(&Med - &Mbe) / 1048576);
  cin.tie(0)->sync_with_stdio(0);
  string str;
  cin >> str;
  cout << str[0] << 'a' << '\n';
  return 0;
}
/*
g++ -std=c++14 -O2 -o 2 2.cpp -Wall -Wextra -Wshadow
-fsanitize=address,undefined -g
*/