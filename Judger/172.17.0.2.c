#include <cstdio>
#include <algorithm>
#include <set>
 
const int MN = 500005;
 
int N, Ans1[MN], Ans2[MN];
struct dat{ int p, h, id; dat() {} dat(int h, int id) : h(h), id(id) {} } a1[MN], a2[MN];
inline bool operator <(dat i, dat j) { return i.h == j.h ? i.id < j.id : i.h < j.h; }
 
std::set<dat> s1, s2;
 
int main() {
    scanf("%d", &N);
    for (int i = 1; i <= N; ++i) scanf("%d", &a1[i].p);
    for (int i = 1; i <= N; ++i) scanf("%d", &a1[i].h);
    for (int i = 1; i <= N; ++i) scanf("%d", &a2[i].p);
    for (int i = 1; i <= N; ++i) scanf("%d", &a2[i].h);
    for (int i = 1; i <= N; ++i) a1[i].id = a2[i].id = i;
    std::sort(a1 + 1, a1 + N + 1, [](dat i, dat j) { return i.p < j.p; });
    std::sort(a2 + 1, a2 + N + 1, [](dat i, dat j) { return i.p < j.p; });
    int cnt = 0;
    for (int i = 0; i <= N; ++i) {
        if (a1[i].p != a1[i + 1].p || a2[i].p != a2[i + 1].p) {
            if (s1.size() < s2.size()) {
                for (auto j : s1) {
                    auto it = s2.lower_bound(dat(j.h, 1));
                    if (it != s2.begin()) {
                        --it, ++cnt;
                        Ans1[cnt] = j.id;
                        Ans2[cnt] = it->id;
                        s2.erase(it);
                    }
                    else return puts("impossible"), 0;
                }
                s1.clear();
            }
            else {
                for (auto j : s2) {
                    auto it = s1.upper_bound(dat(j.h, N));
                    if (it != s1.end()) {
                        ++cnt;
                        Ans2[cnt] = j.id;
                        Ans1[cnt] = it->id;
                        s1.erase(it);
                    }
                    else return puts("impossible"), 0;
                }
                s2.clear();
            }
            if (a1[i].p != a1[i + 1].p)
                for (int j = i + 1; j <= N && a1[j].p == a1[i + 1].p; ++j)
                    s1.insert(a1[j]);
            if (a2[i].p != a2[i + 1].p)
                for (int j = i + 1; j <= N && a2[j].p == a2[i + 1].p; ++j)
                    s2.insert(a2[j]);
        }
    }
    for (int i = 1; i <= N; ++i) printf("%d ", Ans1[i]); puts("");
    for (int i = 1; i <= N; ++i) printf("%d ", Ans2[i]); puts("");
    return 0;
}