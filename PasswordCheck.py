import requests 
import hashlib
import sys


def password_checker(password):
    '''Request Data From the https://haveibeenpwned.com/ API and returns the number of
    times the inputted password has been leaked'''

    hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = hashed_password[:5], hashed_password[5:]
    apiCall = "https://api.pwnedpasswords.com/range/" + first5_char
    request_response= requests.get(apiCall)
    #print(type(request_response))
    if request_response.status_code!= 200:
        raise RuntimeError(f"The request was unsuccessful with Error Code {request_response}, reconfigure api call")
    request_response = (line.split(':') for line in request_response.text.splitlines())
    for h, count in request_response:
        if h == tail:
            return count
    return 0

    
def main():
    password_list = sys.argv[1:]
    for i in password_list:
        num_leaks = password_checker(i)
        if num_leaks == 0:
            print(f"{i},has not been leaked as of yet")
        else:
            print(f"{i}, has been leaked {num_leaks} number of times, change it please")

if __name__ == '__main__':
    main()




