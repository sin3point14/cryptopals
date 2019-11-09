def validate_pkcs7(a): #assuming at least 1 byte padding
    i = 1
    while a[-i] == a[-i-1]:
        i+=1
    if i != a[-1]:
        raise Exception('Invalid PKCS#7 padding')
    return True
if __name__ == "__main__":
    print(validate_pkcs7(b"ICE ICE BABY\x05\x05\x05\x05"))