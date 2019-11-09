#include<fstream>
#include"utils/encoding.h"
#include"utils/xor.h"
int main()
{
    string hex;
    ifstream in("data/chall4.txt");
    pair<char, float> best;
    string beststring;
    best.second = 0;
    while (getline(in, hex)) 
    {
        string byteArray = hex_to_string(hex);
        auto current = detect_single_byte_xor(byteArray);
        if(current[0].second > best.second)
        {
            best = current[0];
            beststring = byteArray;
        }
    }
    cout<<single_byte_xor(beststring, best.first).first<<best.second<<endl;
}