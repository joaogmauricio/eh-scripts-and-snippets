var url = "<URL>";
xhr = new XMLHttpRequest():
xhr.open("POST", url, true);

var boundary = "---------------------------";
boundary += Math.floor(Math.random()*32768);
boundary += Math.floor(Math.random()*32768);
boundary += Math.floor(Math.random()*32768);

xhr.setRequestHeader("Content-Type", "multipart/form-data; boundary=" + boundary);

var body = "";
body += "--";
body += boundary;
body += "\r\n";

body += 'Content-Disposition: form-data; name="fileField"; filename="test.ext"';
body += "\r\n";

// e.g. application/gzip, image/png, etc
body += "Content-Type: <CONTENT_TYPE>";
body += "\r\n";

body += "\r\n";

body += data;
body += "\r\n";

body += "--";
body += boundary;
body += "--";
body += "\r\n";
	
xhr.send(body);
