#include<fstream>
#include"../xor.h"
int main()
{
    string hex;
    ifstream in("data/chall4.txt");
    pair<string, float> best, current;
    best.second = 0;
    while (getline(in, hex)) 
    {
        string byteArray = hex_to_string(hex);
        for(int c = 0; c<128 ;c++)
        {
            current = check(byteArray, c);
            if(best.second < current.second)
                best = current;
        }
    }
    cout<<best.first<<best.second<<endl;
}