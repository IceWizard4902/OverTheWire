<?php
    $defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");
    $modifieddata = array( "showpassword"=>"yes", "bgcolor"=>"#ffffff");
    $originalcookie = "MGw7JCQ5OC04PT8jOSpqdmkgJ25nbCorKCEkIzlscm5oKC4qLSgubjY=";

    function xor_encrypt($in, $key) {
        $text = $in;
        $outText = '';
    
        // Iterate through each character
        for($i=0;$i<strlen($text);$i++) {
        $outText .= $text[$i] ^ $key[$i % strlen($key)];
        }
    
        return $outText;
    }

    function getKey($plain, $cipher) {
        $ciphertext = base64_decode($cipher);
        $plaintext = json_encode($plain);
        $key = xor_encrypt($ciphertext, $plaintext);
        return $key;
    }

    $key = getKey($defaultdata, $originalcookie);
    
    function generateValidPayload($d, $key) {
        $payload = base64_encode(xor_encrypt(json_encode($d), $key));
        return $payload;
    }
    var_dump($key);

    $new = generateValidPayload($modifieddata, "KNHL");
    
    echo $new;
?>