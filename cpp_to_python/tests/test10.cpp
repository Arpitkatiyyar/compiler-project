#include <iostream>
using namespace std;

int main() {
    int i = 1;

    while (i <= 3) {
        int j = 1;

        while (j <= 4) {
            cout << "(" << i << "," << j << ")" << endl;
            j++;
        }

        i++;
    }

    return 0;
}
