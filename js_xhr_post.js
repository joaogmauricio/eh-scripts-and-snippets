var url = "<URL>";
xhr = new XMLHttpRequest():
xhr.open("POST", url, true);

xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

var body = "<BODY>";
xhr.send(body);
