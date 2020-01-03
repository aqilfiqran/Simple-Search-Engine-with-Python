<?php
    $syntax = 'python3 ../Query.py ../../data/index/index.txt ../../data/link/link.txt ';
    if(isset($_GET['t'])){
        $syntax.='-t '.$_GET['t'];
    }
    $command = escapeshellcmd($syntax.' '.$_GET['s']);
    $output=shell_exec($command);
    $datas=json_decode($output,true);
    for($j=0;$j<count($datas);$j++):
        $file = shell_exec('cat ../../data/crawl/'.$datas[$j]['doc']);
        $content = explode("\n",$file);
        $datas[$j]['title']=$content[0];
        $datas[$j]['content']='';
        for($i=1;$i<count($content);$i++):
            $datas[$j]['content'].=$content[$i];
        endfor;
    endfor;
    echo json_encode($datas);
?>
