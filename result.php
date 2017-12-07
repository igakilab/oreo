<DOCTYPE_HTML>
<html>
 <head>
  <title>Shutter Chance!</title>
  <body background="back_logo.png">
  <basefont size="7">
    <p><font size="+7" color="red"><center><u><I>Shutter Chance!!</I></u></center></font></p>
    <?php
      $fp=fopen("/var/www/html/photo/saiten/kekka.txt","r");
      while(($moji=fgetc($fp))!=","){
	$snum = $snum.$moji;
      }
      $all_num=intval($snum); 
      for($i=1;$i<$all_num+1;$i++){
        echo '<img src="photo/saiten/cap'.$i.'.png" width="320" height="180">';
   	print "\n";
     }
    ?>
    <p><font size="+5"color="blue"><center>Point</center></font></p>
    <p><font size="+5"><center><?php
     $fp=fopen("/var/www/html/photo/saiten/kekka.txt","r");
     while(($moji1=fgetc($fp))!=","){
	$smoji1=$smoji1.$moji1;
     }
     while(($moji2=fgetc($fp))!=","){
	$smoji2=$smoji2.$moji2;
     }
     fclose($fp);
     echo $smoji2."/".$smoji1;
     $num1 = intval($smoji1);
     $num2 = intval($smoji2);
     $sump= $num2*100;
     
     echo nl2br("\n");
     echo $sump."pt";
     echo nl2br("\n");
     if($sump<500){
        echo "Dont mind";
     }else if($sump<800){
        echo "great";
    }else{
        echo "excellent";
    }
    ?></center></font><p>
     
  </body>
</html>