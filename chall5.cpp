#include<iostream>
#include"utils/encoding.h"
#include"utils/xor.h"
int main()
{
    string plain =R"(Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal)";
    auto cipher = repeating_xor(plain,"ICE");
    cout<<string_to_hex(cipher.first);
}