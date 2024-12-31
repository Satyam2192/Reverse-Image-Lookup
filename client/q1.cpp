#include <bits/stdc++.h>
using namespace std;

void solve() {
    int t;
    cin >> t;
    
    while (t--) {
        int n;
        cin >> n;

        string row1, row2;
        cin >> row1 >> row2;

        int alvaroWins = 0;

        for (int i = 0; i < n; i += 3) {
            // Check the current 2x3 block
            int aCount = 0;
            // Count 'A' in the current block
            if (row1[i] == 'A') aCount++;
            if (row1[i+1] == 'A') aCount++;
            if (row1[i+2] == 'A') aCount++;
            if (row2[i] == 'A') aCount++;
            if (row2[i+1] == 'A') aCount++;
            if (row2[i+2] == 'A') aCount++;

            // If there are at least 2 'A's, Álvaro wins this district
            if (aCount >= 2) {
                alvaroWins++;
            }
        }

        cout << alvaroWins << endl;
    }
}

int main() {
    solve();
    return 0;
}