#pragma once
#include <map>
#include <set>
#include "InfInt.h"
#include <utility>
#include <algorithm>
using namespace std;
map<char, double>frequency = 
{
    {'a', 0.0651738}, {'b', 0.0124248}, {'c', 0.0217339}, {'d', 0.0349835}, {'e', 0.1041442}, {'f', 0.0197881}, {'g', 0.0158610},
    {'h', 0.0492888}, {'i', 0.0558094}, {'j', 0.0009033}, {'k', 0.0050529}, {'l', 0.0331490}, {'m', 0.0202124}, {'n', 0.0564513},
    {'o', 0.0596302}, {'p', 0.0137645}, {'q', 0.0008606}, {'r', 0.0497563}, {'s', 0.0515760}, {'t', 0.0729357}, {'u', 0.0225134},
    {'v', 0.0082903}, {'w', 0.0171272}, {'x', 0.0013692}, {'y', 0.0145984}, {'z', 0.0007836}, {' ', 0.1918182}

};
bool sort_by_sec(const pair<char,double> &a, const pair<char,double> &b) 
{ 
    return (a.second > b.second); 
} 
int frequency_check(string& s)
{
    double score =0;
    for(int i=0;i<s.length(); i++)
        score += frequency[s[i]];
    return score;
}
pair<string, double> single_byte_xor(string& plain, char c)
{
    string cipher ="";
    double score =0 ;
    for(int i=0;i<plain.length(); i++)
    {
        cipher += plain[i] ^ c;
        score += frequency[cipher[i]];
    }
    return make_pair(cipher,score);
}
vector<pair<char, double>> detect_single_byte_xor(string& cipher)
{
    vector<pair<char, double>> plains;
    for(int i=0; i<128; i++)
        plains.emplace_back(i, single_byte_xor(cipher, i).second);
    sort(plains.begin(), plains.end(), sort_by_sec); 
    return plains;
}
pair<string, double> repeating_xor(string& plain, string key)
{
    string cipher = "";
    double score = 0;
    for(int i=0,j=0; i<plain.length();i++,j=(j+1)%key.length())
    {
        cipher += plain[i] ^ key[j];
        score += frequency[cipher[i]];
    }
    return make_pair(cipher,score);
}
unsigned int count_set_bits(unsigned int n) 
{ 
    unsigned int count = 0; 
    while (n) 
    { 
        count += n & 1; 
        n >>= 1; 
    } 
    return count; 
} 
unsigned int hamming_distance(string s1, string s2)
{
    if(s1.length()!=s2.length())
        return -1;
    unsigned int ham = 0;
    for(int i=0;i<s1.length();i++)
        ham += count_set_bits(s1[i] ^ s2[i]);
    return ham;
}
vector<pair<double, int>> guess_keysize(string cipher, int higher_bound, int lower_bound=1)
{
    vector<pair<double, int>> sorted_keys;
    int length = cipher.length();
    for(int i=lower_bound;i<=higher_bound;i++)
    {
        double score = 0;
        for(int j=0; j+i <= length-1 ; j+=i) 
            for(int k=j+i; k+i <= length-1; k+=i)
                score += hamming_distance(cipher.substr(j, i), cipher.substr(k, i));
        int n= length / i;
        score /= double(i)*(n*(n-1))/2;
        sorted_keys.emplace_back(score, i);
    }
    sort(sorted_keys.begin(), sorted_keys.end());
    return sorted_keys;
}