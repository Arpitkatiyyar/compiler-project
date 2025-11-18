#include <iostream>
using namespace std;

bool check(int a, int b) {
    if (a > 0 && b > 0) {
        return true;
    } else {
        return false;
    }
}

int main() {
    int x = 3;
    int y = -1;

    if (check(x, y) || x > 1) {
        cout << "OK" << endl;
    } else {
        cout << "NOT OK" << endl;
    }

}
