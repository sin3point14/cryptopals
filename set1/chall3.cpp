#include<iostream>
#include"../utils/encoding.h"
#include"../utils/xor.h"
int main(int argc, char *argv[])
{
    if(argc > 2)
    {
        cout<<"Usage- "+string(argv[1])+" <hex_string>"<<endl;
        exit(1);
    }
    string hex=argv[1];
    string byteArray = hex_to_string(hex);
    auto vec = detect_single_byte_xor(byteArray);
    cout<<vec[0].first<<endl<<vec[0].second<<endl<<single_byte_xor(byteArray, vec[0].first).first;
}