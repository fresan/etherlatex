/*
	To be used with the python script for download and compilation
	of latex/bibtex source in Etherpad documents. This script enables
	automation of this process from within a web browser. The
	resulting PDF (or error log) is displayed in the browser.

	Written by Fredrik.Sandin@gmail.com, January 2013.
*/

<?php

/*** Config goes here *****************/
$odr = '/home/USER/PROJECT_FOLDER_WITH_PYTHON_SCRIPT/';
$doc = 'DOCUMENT_NAME';
/**************************************/

$pdf = $odr . $doc . '.pdf';
$err = $odr . $doc . '.err';
$cmd = $odr . $doc . '.py';

$ret = (int)shell_exec($cmd .' > /dev/null; echo $?');

if ($ret==0 && file_exists($pdf)) {
    header('Content-Type: application/pdf');
    header('Content-Transfer-Encoding: binary');
    header('Expires: 0');
    header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
    header('Pragma: public');
    header('Content-Length: ' . filesize($pdf));
    ob_clean();
    flush();
    readfile($pdf);
    exit;
} else {
    header('Content-Type: text/html; charset=utf-8');
    header('Content-Transfer-Encoding: binary');
    header('Expires: 0');
    header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
    header('Pragma: public');
    header('Content-Length: ' . filesize($err));
    ob_clean();
    flush();
    if(file_exists($err)) {    
	echo $ret;
	echo nl2br(htmlentities(file_get_contents($err)));
    } else {
	echo "Could not read output files, contact the server administrator.\n";
    }
    exit;
}

?>
