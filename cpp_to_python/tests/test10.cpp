#include <iostream>
using namespace std;

int main() {
    int x = 10;
    int y = 5;

    if (x > 0) {
        cout << "x is positive" << endl;

        if (y > 0) {
            cout << "y is also positive" << endl;

            if (x > y) {
                cout << "x is greater than y" << endl;
            } else {
                cout << "y is greater or equal to x" << endl;
            }

        } else {
            cout << "y is non-positive" << endl;
        }

    } else {
        cout << "x is non-positive" << endl;
    }

    return 0;
}
