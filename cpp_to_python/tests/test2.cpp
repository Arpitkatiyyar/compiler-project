#include <iostream>
using namespace std;

int main() {
    int x = 0;
    int y = 0;

    cout << "Enter x:";
    cin >> x;
    
    cout << "Enter y:";
    cin >> y;

    int sum = x + y;
    int mul = x * y;

    cout << "sum=" << sum << " mul=" << mul << endl;

    return 0;
}
