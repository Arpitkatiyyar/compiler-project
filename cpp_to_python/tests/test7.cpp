#include <iostream>
using namespace std;

int add(int a, int b) {
    return a + b;
}

int main() {
    int x = 5;
    int y = 7;
    int result = add(x, y);

    cout << "result=" << result << endl;

    return 0;
}
