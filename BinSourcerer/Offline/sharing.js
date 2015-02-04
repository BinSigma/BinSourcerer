function getTweetURL(hostName) {
    var url = document.createElement('a');
    url.href = window.location.href;
    var pathname = url.pathname[0] === '/' ? url.pathname : '/' + url.pathname;
    var sUrl=hostName + pathname + url.search;
    var titleElement = document.title;
    window.open("https://twitter.com/intent/tweet?&text="+titleElement+"&url="+encodeURIComponent(sUrl));
}

function getGooglePlusURL(hostName) {
    var url = document.createElement('a');
    url.href = window.location.href;
    var pathname = url.pathname[0] === '/' ? url.pathname : '/' + url.pathname;
    var sUrl=hostName + pathname + url.search;
    var titleElement = document.title;
    window.open("https://plus.google.com/share?url="+encodeURIComponent(sUrl));
}
