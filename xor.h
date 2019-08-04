#pragma once
#include<map>
#include"InfInt.h"
#include<utility>
using namespace std;
map<char, float>frequency = 
{
    {'a', 0.0651738}, {'b', 0.0124248}, {'c', 0.0217339}, {'d', 0.0349835}, {'e', 0.1041442}, {'f', 0.0197881}, {'g', 0.0158610},
    {'h', 0.0492888}, {'i', 0.0558094}, {'j', 0.0009033}, {'k', 0.0050529}, {'l', 0.0331490}, {'m', 0.0202124}, {'n', 0.0564513},
    {'o', 0.0596302}, {'p', 0.0137645}, {'q', 0.0008606}, {'r', 0.0497563}, {'s', 0.0515760}, {'t', 0.0729357}, {'u', 0.0225134},
    {'v', 0.0082903}, {'w', 0.0171272}, {'x', 0.0013692}, {'y', 0.0145984}, {'z', 0.0007836}, {' ', 0.1918182}

};
string hex_to_string(string hex)
{
    int len = hex.length();
    string newString;
    for(int i=0; i< len; i+=2)
    {
        string byte = hex.substr(i,2);
        char chr = (char) (int)strtol(byte.c_str(), NULL, 16);
        newString.push_back(chr);
    }
    return newString;
}
pair<string, float> check(string s, char c)
{
    float score =0;
    for(int i=0;i<s.length(); i++)
    {
        s[i] = s[i] ^ c;
        score += frequency[s[i]];
    }
    return make_pair(s, score);
}