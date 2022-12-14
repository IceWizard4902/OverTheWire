<div align="center">
  <h1>Natas</h1>
</div>

- [Natas 0](#natas-0)
- [Natas 1](#natas-1)
- [Natas 2](#natas-2)
- [Natas 3](#natas-3)
- [Natas 4](#natas-4)
- [Natas 5](#natas-5)
- [Natas 6](#natas-6)
- [Natas 7](#natas-7)
- [Natas 8](#natas-8)
- [Natas 9](#natas-9)
- [Natas 10](#natas-10)
- [Natas 11](#natas-11)
- [Natas 12](#natas-12)
- [Natas 13](#natas-13)
- [Natas 14](#natas-14)
- [Natas 15](#natas-15)

# Natas 0 

Simple Inspect Element of the page will reveal the password in the comment of the HTML.

natas1: `g9D9cREhslqBKtcA2uocGHPfMZVzeFK6`

# Natas 1

Instead of right-clicking, one can invoke Inspect Element by using the keyboard combination `Ctrl + Shift + I`. Password again will be in the comment of the HTML.

natas2: `h4ubbcXrWqsTo7GGnnUMLppXbOogfBZ7`

# Natas 2

Viewing the page source, there is indeed nothing on the page itself. However, there is a image with the path of `files/pixel.png` displayed on the page. 

We inspect `files` directory by going to `http://natas2.natas.labs.overthewire.org/files/`. In here we can see two files, `pixel.png` from the page and a new file `user.txt`. Opening `user.txt` should give us the password for the user `natas3` for the next level. 

natas3: `G6ctbMJ5Nb4cbFwhpMPSvxGHhQ7I6W8Q`

# Natas 3

Viewing the source of the web page, again, there is indeed nothing. But there is a very interesting comment: `No more information leaks!! Not even Google will find it this time...`. This implies that Google crawler will not touch whatever the so-called "information leaks". 

We can think of `robots.txt` in this case. A `robots.txt` file tells search engine crawlers which URLs the crawler can access on your site. To disallow crawlers/bots accessing some sensitive data on your site, one can put there the disallowed lists of URLs on the page.

Accessing `robots.txt`, we found out that there is a interesting disallowed URL: `/s3cr3t`. Going to this URL, we can see that, again, there is a `user.txt` file there. Inside the `user.txt` is the password for the next stage.

natas4: `tKOcJIbzM4lTs8hbCmzn5Zr4434fGZQm`

# Natas 4

Solving this requires Burp Suite to modify the HTTP header in the request to the server.

Upon going to the webpage, we are greeted with the message of `Access disallowed. You are visiting from "" while authorized users should come only from "http://natas5.natas.labs.overthewire.org/"`

The page has a `Refresh page` link to click on. Clicking on that, the page rendered will have a different message: `Access disallowed. You are visiting from "http://natas4.natas.labs.overthewire.org/" while authorized users should come only from "http://natas5.natas.labs.overthewire.org/"`. We are now at the `/index.php` page.

Clicking the button once more will display a different message `Access disallowed. You are visiting from "http://natas4.natas.labs.overthewire.org/index.php" while authorized users should come only from "http://natas5.natas.labs.overthewire.org/"`

Hence, there is something that has to do with the request that is invoked when we clicked on the `Refresh page` link. After refresh the page (not by using the link but the original link to `natas4`), we can see that every time we click on the `Refresh page`, the `Referer` field in the HTTP header changes, and what is in the `Referer` will be displayed on the web page. 

From the Mozilla docs, "The Referer HTTP request header contains an absolute or partial address of the page that makes the request. The Referer header allows a server to identify a page where people are visiting it from. This data can be used for analytics, logging, optimized caching, and more".

Therefore, to access the password, we need to change the `Referer` field to `http://natas5.natas.labs.overthewire.org/`. After doing it using the Intercept functionality in Burp Suite and forward the modified HTTP request, we can obtain the password. 

natas5: `Z0NsrtIkJoKALBCLi5eqFfcRN82Au2oD`

# Natas 5

We are not logged in. One way for web page to authenticate users (as HTTP is stateless) is by using cookies. Opening the Devtools from Chrome and navigate to the `Network` tab, then we refresh the page, we can observe that there is a cookie with the content of `loggedin=0` in the HTTP header. 

Hence, to authenticate, we have to change the value of the cookie from `0` to `1`. We can easily do this by using the `Application` tab, navigate to a dropdown named `Cookies`, then double click on the value `0`, change it to `1`. Refresh the web page and we should obtain the password.

natas6: `fOIvE0MDtPTgRhqmmvvAOt2EfXR6uQgR`

# Natas 6

From the code, we can observe that the secret is loaded from the resource located at `includes/secret.inc`. Going to that resource will give us the secret. Key in the secret and we should get the password to the next stage

natas7: `jmxSiH3SP6Sonf8dv66ng8v1cIEdjXWr`

# Natas 7 

Clicking on the `Home` and `About`, we can see that the HTTP parameter `page` changes to whatever the value is there. Hence we can take advantage of this to read any file on the system. We have the hint (when we view the source of the web page) that the password is at `/etc/natas_webpass/natas8`. 

Key in that value into the `page` parameter, we should be able to retrieve the password. The URL to access the password will be `http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8`

natas8: `a6bZCNYwdKqN5cGP11ZdtPg0iImQQhAB`

# Natas 8

Looking at the code, we have the encoded secret and how the secret is encoded. To get the secret, we unroll the encoding process. The string will first be converted to the `bin` format, then reverse, then decode from `Base64`. `Cyberchef` can easily help us here, with 3 layers being `From Hex`, `Reverse` and `From Base64`. The secret derived from the decoding is `oubWYf2kBq`.

Inputting the secret to the form should give us the password to the next level.

natas9: `Sda6t0vkOPkM8YeOZkAGVhFoaplvlJFd`

# Natas 9 

Our target is in the file at `/etc/natas_webpass/natas10`.

From the source code, the content in the form that we submitted is put into the command in the `passthru` call. 

The command that is executed on the server is `grep -i $key dictionary.txt`, where `$key` is the input that we submitted. We have total control on the content of the command pass to the `passthru` call. Hence, what we can do is to `grep` everything in the `/etc/natas_webpass/natas10` file, and disregard everything in the `dictionary.txt` file.

Inputting `.` to the `dictionary.txt` file, basically we are matching everything, we can see that there is nothing related to the password for the next level that is stored in here. Indeed, searching for any strings of length from 15 to 20 using `-x '.\{20,32\}'` does not yield anything really interesting. 

Hence, we can "escape" the call of `grep` on `dictionary` by doing `. /etc/natas_webpass/natas10; grep "!" `. This executes two commands, as the `;` is specified. First, it tries to do `grep -i . /etc/natas_webpass/natas10` - basically matching anything in the file. Then it tries to `grep` strings that contain `!` in it, and there are no such strings. The latter command is there to prevent the content of `dictionary.txt` clogging up the result. Inputting the payload, we should retrieve the password for the next level.

natas10: `D44EcsFkLxPIkAAKLosx8z3hxX1Z4MCE`

# Natas 10

Same idea, but this time we cannot use the `;` trick to make the result less clogged. `grep` does work on two files, and the filtering does not block the `/` character, hence we can just put `. /etc/natas_webpass/natas11 `. The `grep` command ran will match any character in both `/etc/natas_webpass/natas11` and `dictionary.txt`. 

The first entry of the result of this command should yield the password to the next level. Indeed, that is `/etc/natas_webpass/natas11:1KFqoJXi6hRaPluAmk8ESDW4fSysRoIg`.

natas11: `1KFqoJXi6hRaPluAmk8ESDW4fSysRoIg`

# Natas 11

Viewing the source code, we can deduct a few things: 

- The `defaultData` is being encrypted with `xor` with a hard-coded key in the `xor_encrypt` function. The result of the encryption (as performed by the `saveData` function) will be stored in the cookie of the page.
- After the first load, cookies from the user will be checked in the `loadData` function. If the data can be decoded and decrypted, it will be stored into the local `data` variable. The data will be of the same structure as that of `defaultdata`. 
- If the `showpassword` field of the `data` array gives `"yes"`, then the password will be displayed to the current level's page.

The code for the operations mentioned below is in the [natas11.php](natas11.php).

What we need to do is to craft a valid cookie value, such that when it is decoded and decrypted on the server side, it will generate an entry of `array( "showpassword"=>"yes", "bgcolor"=>"#ffffff")`. Note that `bgcolor` does not matter in the checking.

To figure out the key of the `xor` encryption, we can do the `xor` operation on the plaintext (the JSON encoded string of the `defaultdata`) and the ciphertext (the value of `"data"` in the cookie). This is because of the way `xor`, or one-time pad works: 

```
ciphertext = plaintext xor key
ciphertext xor plaintext = plaintext xor key xor plaintext
ciphertext xor plaintext = key
```

The key, after doing these operations, is `KNHL`. The key is repeated due to the way that the `xor` operation in the `xor_encrypt`, each 4 characters in the plaintext will be `xor`-ed with the key. Hence, in the result of the code in [natas11.php](natas11.php), you can see that the `KNHL` string is repeated multiple times.

With the key, we can easily generate the correct payload to retrieve the password. In [natas11.php](natas11.php), the target plaintext is the array `array( "showpassword"=>"yes", "bgcolor"=>"#ffffff")`. We follow the way that the original PHP code encode and encrypt the array to generate the payload. Changing the cookie value to the payload, then after submitted the form we can retrieve the flag.

Payload is `MGw7JCQ5OC04PT8jOSpqdmk3LT9pYmouLC0nICQ8anZpbS4qLSguKmkz`

natas12: `YWqo0pjpcXzSIl5NMAVxg12QxeC1w9QG`

# Natas 12

There is no checking in the source code that the uploaded file must be a JPEG file, hence we can upload any file that we want to the server. Since the backend is running on PHP, we might as well upload a PHP file to get the content of the file in `/etc/natas_webpass/natas13`. The file we will upload is in the [natas12.php](natas12.php).

However, after uploading the file, the file name got changed to `<some_random_string>.jpg`, which disallows the PHP code from executing. Inspecting further, we can observe that there is a hidden `filename` (which determines the file name uploaded to the server), and it is already determined before any file is chosen. This `filename` is the path of the uploaded file on the web server.

Hence, if we can change the `filename` extension back to `.php`, we can make the PHP code valid and retrieve the flag. Opening the browser from Burp Suite, and then choose the PHP payload file and turn the Burp Suite intercept on, we can see the form data uploaded will be something like

```
------WebKitFormBoundaryEex9eRjYhKzAHvH7
Content-Disposition: form-data; name="MAX_FILE_SIZE"

1000
------WebKitFormBoundaryEex9eRjYhKzAHvH7
Content-Disposition: form-data; name="filename"

j6s2vxhm9i.jpg
------WebKitFormBoundaryEex9eRjYhKzAHvH7
Content-Disposition: form-data; name="uploadedfile"; filename="natas12.php"
Content-Type: application/octet-stream

<?php
    passthru("cat /etc/natas_webpass/natas13")
?>
------WebKitFormBoundaryEex9eRjYhKzAHvH7--
```

We change the `.jpg` filename to `natas12.php`, or any filename with the `.php` extension. Sent the changed POST request to the server, the path to the uploaded `.php` file should appear on the web page. Clicking on the link will lead to the result of executing `.php` file, which is the password of the next level.

natas13: `lW3jYRI02ZKDBb8VtQBU1f6eDRo6WEj9`

# Natas 13

Same idea, but this time there is an additional check in `exif_imagetype`, which only reads the first bytes of a file to check its signature (or in other words, check the Magic Number of the file). We hence have to put the magic number of image files to the header of the PHP file. PHP file does not really complain if there is some text before the `php` code portion. 

We can pick `GIF`, it is a valid type for a image. GIF has the magic number, in ASCII of `GIF89a`. Put this before the `php` portion of the code and we should be able to bypass the check.

Again, turn on the Burp Suite browser and the Proxy Intercept function. Change the `filename` of the POST request form to anything ends with `.php`. An example, in the payload portion of the POST request, can be: 

```
------WebKitFormBoundarya8snrslosPiK9vI2
Content-Disposition: form-data; name="MAX_FILE_SIZE"

1000
------WebKitFormBoundarya8snrslosPiK9vI2
Content-Disposition: form-data; name="filename"

9q708avz39.php
------WebKitFormBoundarya8snrslosPiK9vI2
Content-Disposition: form-data; name="uploadedfile"; filename="natas13.php"
Content-Type: application/octet-stream

GIF89a
<?php
    passthru("cat /etc/natas_webpass/natas13")
?>
------WebKitFormBoundarya8snrslosPiK9vI2--
```

Following the link to the uploaded resource, we can see the GIF magic number that we prepend to the PHP code and the result of the command in `passthru()`

natas14: `qPazSJBmrmU7UQJv17MHk1PGC4DxZMEP`

# Natas 14

To get the password for the next level, the result of the query 
``` sql
SELECT * from users where username=\"".$_REQUEST["username"]."\" and password=\"".$_REQUEST["password"]."\"
```
must return the result consisting of one or more lines (the check is at `mysqli_num_rows`). We obviously have no clue what is in the database, indeed any attempt in trying the `username` of `natas14` or `natas15` does not work.

This code is vulnerable to SQL injection, as we can directly manipulate the query to whatever we want. Also there is a debug function to help us out, by putting the URL parameter of `debug` in the POST request to the server. Submitting the form will do a POST request to the endpoint at `/index.php`. Hence, to enable the debug mode to see our command (which is very useful), we can use the intercept functionality, along with the in-app browser of Burp Suite to manipulate the URL parameter in the POST request to the backend.

We have no idea of the password in the database, hence we need a way to escape the query. Doing `"` at the beginning closes the first quotation mark in the `username` field. Of course no username matches `""` (empty string), hence we need a condition that is always True. Looking up on Google, we can see one common way is to put `or true` in the payload to make the result of the query always True. To escape all the conditions at the end of the query, again from simple Googling, we can use the comment in `mysql`: `--`. In MySQL, the `--`  (double-dash) comment style requires the second dash to be followed by at least one whitespace or control character (such as a space, tab, newline, and so on).

From all of the information above, our username field will be `" or true;-- ` (notice the space after the double-dash). The password field can be anything, due to the double dash `--` everything in the `password` comparison will be ignored anyways. I put `abcd` as the password. The query will become:

```sql
SELECT * from users where username="" or true;-- " and password="abcd"
```

Sending this using the in-app browser from Burp Suite, and change the POST endpoint to `/index.php`. The request will be something like 

```
POST /index.php?debug HTTP/1.1
Host: natas14.natas.labs.overthewire.org
Content-Length: 42
Cache-Control: max-age=0
Authorization: Basic bmF0YXMxNDpxUGF6U0pCbXJtVTdVUUp2MTdNSGsxUEdDNER4Wk1FUA==
Upgrade-Insecure-Requests: 1
Origin: http://natas14.natas.labs.overthewire.org
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://natas14.natas.labs.overthewire.org/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

username=%22+or+true%3B--+++&password=abcd
```

We should get the password after forwarding this POST request, and also see the SQL command being executed.

natas15: `TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB`

# Natas 15

Tough challenge, but simple concept. This is an example (sort) of Blind SQL injection. 

For a query, the PHP backend returns `"This user exists."` if the result of the query has more than 0 rows, otherwise it returns `"This user doesn't exist.`. There is no additional information to retrieve the password, and the only interaction we are allowed is on the SQL database, therefore we can assume that the password for the next level exists in the SQL database.

Putting `natas16` as the first username, we are informed that the user `natas16` indeed exists. We now need a way to make the query result "leak" something about the password. We have free rein on controlling the input, or the query itself, hence we can make more specific queries involving the password.

Since we do not know the password, we can start guessing letter by letter. We can employ the `%` symbol in MySQL. For instance, `abcd%` will match any strings start with `abcd`. Using this, the username field we submitted will look something like `natas16" and password like binary abcd%`. `binary` in MySQL means that the strings matched will be case-sensitive (this is needed as the password is a mix of lowercase and uppercase characters). The query in the PHP backend will look something like

```sql
SELECT * from users where username="natas16" and password like binary abcd%";
```

Initially, we know nothing about the password, hence we start from `<guess_char>%`. `guess_char` is the character we are guessing in the first position, the guess space is all the alphanumeric characters. The correct guess will return the response of `"This user exists."`. Let's say the character in the first position of the password is `T`, the next guess of the password is going to be `T<guess_char>%`. We will repeat this procedure until the length of the string preceding the `%` sign is equal to 32 (the size of all the password in all of the levels). 

To make the process less tedious, we can use the Intruder functionality from Burp Suite, but unfortunately Burp Suite has very silly rate limiting and throttling if you did not purchase a license. OWASP Zap is another candidate, but again, unfortunately the process of guessing on OWASP Zap using the Fuzz functionality is very tedious with 32 character strings. Therefore, to generate the guess fast and smartly, we can employ Python `requests` library to do the job.

As brute-forcing the entire set of alphanumeric characters for every position in the password string takes considerable time (lots of overhead with establishing connection with challenge server), we can narrow down the search space by only searching on the set of characters that actually appear in the password. We can use the double `%` in MySQL to do the work. `%a%` matches any string that contains the letter `a`. Hence, we can traverse through the list of all alphanumeric characters, and check whether it exists in the password of the user `natas16`. The SQL query to check if the character `T` exists in the password will look like this, note that `binary` is also used to respect the case-sensitiveness of the password:

```sql
SELECT * from users where username="natas16" and password like binary %T%"
```

The username field will look something like `natas16" and password like binary %T%`. After generating the trimmed down character set, we can proceed to guessing the character in every position of the password with the idea given above. 

The code for all of the aforementioned operation is in [natas15.py](natas15.py). 

natas16: `TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V`