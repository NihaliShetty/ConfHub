<?php
extract($_GET);
$file = fopen("Interests.txt","r");
$data = fgets($file);
while(!feof($file))
{
    $line = trim(fgets($file));
    if(strncasecmp($line,$term,strlen($term))==0)
    {
        $res[] = $line;
    }
}

echo json_encode($res);
?>