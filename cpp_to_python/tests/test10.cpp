#include <iostream>
using namespace std;

int factorial(int n) {
    int f = 1;
    for (int i = 1; i < n + 1; i++) {
        f = f + (f * (i - 1));
    }
    return f;
}


int fibonacci(int n) {
    int a = 0;
    int b = 1;
    int temp = 0;

    for (int i = 1; i < n + 1; i++) {
        temp = a + b;
        a = b;
        b = temp;
    }
    return a;
}


int sumSquares(int n) {
    int s = 0;
    for (int i = 1; i < n + 1; i++) {
        s = s + (i * i);
    }
    return s;
}



int compute(int x, int y, int z) {
    int fact = factorial(x);
    int fib = fibonacci(y);
    int sq  = sumSquares(z);
   
    int result = fact + fib + sq ;
    return result;
}


int main() {
    int x=0;
    int y=0;
    int z=0;
    cout << "Enter x: ";
    cin >> x;
    cout << "Enter y: ";
    cin >> y;
    cout << "Enter z: ";
    cin >> z;
    cout << "Processing..." << endl;
    int output = compute(x, y, z);
    cout << "Final Output = " << output << endl;
}
