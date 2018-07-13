<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>&quot;Shutter Chance!!;</title>

<link rel="stylesheet" type="text/css" href="./assets/css/styles.css" />
<link rel="stylesheet" type="text/css" href="./assets/jquery.shutter/jquery.shutter.css" />

</head>
<body>

    <div id="top"></div>

    <div id="page">

        <h1>Shutter Chance!!</h1>

        <h2><p><font size="+5"><center><?php
     $fp=fopen("/var/www/html/photo/saiten/kekka.txt","r");
     while(($moji1=fgetc($fp))!=","){
	$smoji1=$smoji1.$moji1;
     }
     while(($moji2=fgetc($fp))!=","){
	$smoji2=$smoji2.$moji2;
     }
     fclose($fp);
     $num1 = intval($smoji1);
     $num2 = intval($smoji2);
     $sump= $num2*100;
     $score = $num2 / $num1 *100;
     $score = round($score,1);
     $score2 = "<span style='color:yellow'> $score % </span>";
     echo $score2;					  
					  
     echo nl2br("\n");
     if($score<=50){					      
          echo '<font color="blue">Dont mind</font>';
     }else if($score<75){
        echo '<font color="Green">Great!</font>';
    }else{
        echo '<font color="red">Excellent</font>';
    }
    ?></center></font><p></h2>

        <div id="container">
            <div id="photo"></div>
        </div>



        <p class="credit">Photos used in this demo: <a href="http://www.flickr.com/photos/zanthia/5429569236/">Hohenschwangau</a>, <a href="http://www.flickr.com/photos/zanthia/5393654169/">Erg Chebbi</a>, <a href="http://www.flickr.com/photos/axelhartmann/5405452502/">1500-in front of</a>, <a href="http://www.flickr.com/photos/gnuckx/5386807102/">Circolo Nautico</a></p>

        <!-- You are free to remove this footer -->

        <div id="footer">
            <h2>Shutter Chance!!</h2>
            <a class="tzine" href="http://tutorialzine.com/2011/03/photography-portfolio-shutter-effect/">Read &amp; Download on</a>
        </div>

    </div>

    <script>
        var hoge = document.getElementById('hoge');

        hoge.innerHTML = '<font color="red">hogehoge</font>';

    </script>
     <?php
      $fp=fopen("/var/www/html/photo/saiten/kekka.txt","r");
      while(($moji=fgetc($fp))!=","){
	$snum = $snum.$moji;
      }
      $all_num=intval($snum); 
      //for($i=1;$i<$all_num+1;$i++){
        //echo '<img src="photo/saiten/cap'.$i.'.png" width="320" height="180">';
   	//print "\n";
     //}
    ?>

    <script>
            var myPhoto = document.getElementById('photo');
	    var num = <?php echo $all_num;?>;
            //var fs = new ActiveXObject("Scripting.FileSystemObject");
            //var file = fs.OpenTextFile("assets/img/photos/Photo_test.txt");
            //text1 = Number(file.ReadLine());
            //text2 = Number(file.ReadLine());
        var text = '<ul>';
        for (var i = 1; i <= num; i++) {
            Photo_Pass = "" + i + ".png";
            text += '<li><img src= "photo/saiten/cap' + Photo_Pass + '" width="640" height="400" alt="Landscape" /></li>';
        }
          text += '</ul>';
        myPhoto.innerHTML = text;
        //myPhoto.innerHTML = '<ul><br><li><img src= "assets/img/photos/1.jpg" width="640" height="400" alt="Landscape" /></li><br><li><img src= "assets/img/photos/2.jpg" width="640" height="400" alt="Landscape" /></li><br><li><img src= "assets/img/photos/3.jpg" width="640" height="400" alt="Landscape" /></li><br></ul><br>';
			     </script>

    
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.0/jquery.min.js"></script>
    <script src="assets/jquery.shutter/jquery.shutter.js"></script>
    <script src="assets/js/script.js"></script>

</body>
</html>

