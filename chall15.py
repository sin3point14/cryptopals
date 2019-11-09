def validate_pkcs7(a): #assuming at least 1 byte padding
    i = 1
    while a[-i] == a[-i-1]:
        i+=1
    if i != a[-1] or i > 16:
        #raise Exception('Invalid PKCS#7 padding')
        return False
    return True
if __name__ == "__main__":
    print(validate_pkcs7(b"ICE ICE BABY"+bytes([5])*4))
    print(validate_pkcs7(b"A"*16+bytes([16])*16))