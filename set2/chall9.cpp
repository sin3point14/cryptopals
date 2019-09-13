#include<iostream>
#include"../utils/encoding.h"
using namespace std;
string pkcs7_padding (string text, int padding){
    int l = padding - text.length() % padding;
    string padded = text;
    for(int i=0 ; i<l;i++)
        padded += char(l);
    return padded;
}
int main(){
    string text = "YELLOW SUBMARINE";
    cout<<string_to_hex(pkcs7_padding(text, 20));
}