#include<iostream>
#include"../xor.h"
int main(int argc, char *argv[])
{
    if(argc > 2)
    {
        cout<<"Usage- "+string(argv[1])+" <hex_string>"<<endl;
        exit(1);
    }
    string hex=argv[1];
    string byteArray = hex_to_string(hex);
    pair<string, float> best, current;
    best.second = 0;
    for(int c=0;int(c)<127;c++)
    {
        current = check(byteArray, c);
        if(best.second < current.second)
            best = current;
    }
    cout<<best.first<<endl<<best.second<<endl;
}