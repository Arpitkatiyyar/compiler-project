// 1
// #include<iostream>
// using namespace std;
// int main(){
//     int a=3;
//     int b=5;
//     int c=a+b;
//     cout<<c;
// }


//2
// #include<iostream>
// using namespace std;
// int main(){
//     int a=4;
//     int b=7;
//     if(a>b){
//         cout<<a;
//     }
//     else{
//         cout<<b;
//     }
// }

//3
// #include<iostream>
// using namespace std;
// int main(){
//     int a=4;
//     if(a%2==0){
//         cout<<"EVEN";
//     }
//     else{
//         cout<<"odd";
//     }
// }

//4
// # include<iostream>
// using namespace std;
// int main(){
//     int a=2;
//     int b=3;
//     int c=4;
//     if(a<b){
//         if(b<c){
//             cout<<"A";
//         }
//         else{
//             cout<<"B";
//         }
//     }
//     else{
//         cout<<"C";
//     }
// }

//5
// #include<iostream>
// using namespace std;
// int main(){
//     for(int i=0;i<5;i=i+1){
//         cout<<i;
//     }
// }

//6
// #include<iostream>
// using namespace std;
// int main(){
//     for(int i=0;i<5;i=i+1){
//         for(int j=0;j<6;j=j+1){
//             cout<<i;
//             cout<<j;
//         }
//     }
// }


//7
// #include<iostream>
// using namespace std;
// int main(){
//     int i=0;
//     while(i<5){
//         cout<<i;
//         i=i+1;
//     }
// }

// 8
// #include <iostream>
// using namespace std;
// int main(){
//     int a=3;
//     int b=5;
//     int c=7;
//     int d=9;
//     int e=a+b*c/d;
//     cout<<e;
// }

//9
// #include <iostream>
// using namespace std;
// int main(){
//     int a=0;
//     int b=0;
//     cout<<"Enter A & B:"<<endl;
//     cin>>a;
//     cin>>b;
//     int c=a+b;
//     cout<<c;
// }

//10
// #include <iostream>
// using namespace std;

// int add(int a, int b) {
//     return a + b;
// }

// int main() {
//     int n = 2;
//     int x = 0;
//     int y = 0;
//     cout << "Enter x: ";
//     cin >> x;
//     cout << "Enter y: ";
//     cin >> y;
//     for (int i = 0; i < 3; i++) {
//         cout << "i=" << i << endl;
//     }
//     int s = add(x, y);
//     cout << "sum=" << s << endl;
//     return 0;
// }

// 11
// #include<iostream>
// using namespace std;
// int main(){
//     int x=4;
//     int y=7;
//     int z=3;
//     if(x<y){
//         if(y<z){
//             cout<<"y is greater";
//         }
//         else{
//             cout<<"y is less than z";
//         }
//     }
//     else {
//         cout<<"y is greater";
//     }
// }
//12

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
