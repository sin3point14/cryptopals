import requests

inc_time = 0.02

def pwn(url, hash_len):
    global inc_time
    pwned_hash = ""
    prev_time = requests.get(url, params={"file": "lol","signature": "X" }).elapsed.total_seconds()
    for _ in range(1,hash_len+1):
        for i in "0123456789abcdef":
            payload = pwned_hash + i
            t = requests.get(url, params={"file": "lol","signature": payload + 'X'*len(payload) }).elapsed.total_seconds()
            print(t, payload)
            if t > prev_time+inc_time:
                pwned_hash+=i
                prev_time = t
                break
    print(pwned_hash)
    return(pwned_hash)

# hash_len = length of hash in hex
print("PWNED - " + pwn("http://localhost:8082/test", 40))