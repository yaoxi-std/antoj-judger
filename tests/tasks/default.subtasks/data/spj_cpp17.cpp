#include "testlib.h"
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
int main(int argc, char* argv[]) {
  registerTestlibCmd(argc, argv);
  string x = ouf.readToken();
  string y = ans.readToken();
  if (x == y) {
    quitf(_ok, "aCCePteD");
  } else if (x.size() == 2 && y.size() == 2 && x[0] == y[1] && x[1] == y[0]) {
    cerr << "shuodedaoli.\n";
    quitp(50, "sWAP");
  } else {
    quitf(_wa, "wRoNG");
  }
  return 0;
}
/*
g++ -std=c++14 -O2 -o spj_cpp17 spj_cpp17.cpp -Wall -Wextra -Wshadow
-fsanitize=address,undefined -g
*/