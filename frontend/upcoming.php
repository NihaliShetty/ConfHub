<?php
extract($_GET);
$file = file_get_contents("list_of_conf.txt","r");
// fseek($file);
// $data = fread($file);
// echo $data;
echo $file;
?>