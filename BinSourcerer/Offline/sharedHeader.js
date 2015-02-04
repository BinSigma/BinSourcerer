function getActionURL() {
    var form1 = document.getElementById('searchForm');
    var orginalHref = window.location.href;
    var urlStr = orginalHref.substring(0, orginalHref
    	    .indexOf(window.location.search));
    var newHref = "";
    var s = encodeURIComponent(form1.s.value);

    var keepFilterSelection = document.getElementById('selection');
    var ff;
    if (keepFilterSelection) {
        ff = keepFilterSelection.checked;
    } else {
        ff = "";
    }
    var theSrchStrg = location.search;
    var re = /(?:\?|&(?:amp;)?)([^=&#]+)(?:=?([^&#]*))/g,
        match, params = {},
        decode = function (s) {return decodeURIComponent(s.replace(/\+/g, " "));};
    var params = "";

    var firstElement = true;
    while (match = re.exec(theSrchStrg)) {
        var pName = decode(match[1]);
        var pValue = decode(match[2]);
        if (pValue) {
            if(pName != 'filterChecked' && pName != 'ml' && pName != 'mp' && pName != 'me' && 
                    pName != 'md' && pName != 'ipid' && pName != 'p' && pName != 's' && 
                    pName != 'fid' && pName != 'cid' && pName != 'pid' && pName != 'did' && pName != 'prevcid' ) {
                if (firstElement) {
                    firstElement = false;
                    params = "&" + pName + "=" + encodeURIComponent(pValue);
                } else {
                    params = params + "&" + pName + "=" + encodeURIComponent(pValue);
                }
            }
            if (document.getElementById("selection") == null && 
                    (pName == 'filterChecked' || pName == 'ml' || pName == 'mp' || pName == 'md' || pName == 'me')) {
                if (firstElement) {
                    firstElement = false;
                    params = "&" + pName + "=" + encodeURIComponent(pValue);
                } else {
                    params = params + "&" + pName + "=" + encodeURIComponent(pValue);
                }
            }
        }
    }
					    
    newHref = "search?s="+s;
    if(document.getElementById("selection") != null && !document.getElementById("selection").checked){
        window.location.href = newHref + createMoreLessParamString() + "&filterChecked=false";
    }
    else if(document.getElementById("selection") != null && document.getElementById("selection").checked){
        window.location.href = newHref + params + createMoreLessParamString() + "&filterChecked=true";
    }else{
        window.location.href = newHref+params;						
    }
	
    return false;
}

function passCheckedFilters(s1,id) {
    var theSrchStrg = location.search;
    var re = /(?:\?|&(?:amp;)?)([^=&#]+)(?:=?([^&#]*))/g,
        match, params = {},
        decode = function (s) {return decodeURIComponent(s.replace(/\+/g, " "));};
      					
    var params = "";
    var newHref = "";
    var firstElement = true;
    while (match = re.exec(theSrchStrg)) {
        var pName = decode(match[1]);
        var pValue = decode(match[2]);
        if (pValue) {
            if(pName != 'filterChecked' && pName != 'ml' && pName != 'mp' && pName != 'md' && 
                    pName != 'me' && pName != 'ipid' && pName != 'p' && pName != 's' && 
                    pName != 'fid' && pName != 'cid' && pName != 'rid' && pName != 'pid' && pName != 'did' && 
                    pName != 'pg' && pName != 'prevcid' && pName != 'prevdid') {
                if (firstElement) {
                    firstElement = false;
                    params = "&" + pName + "=" + encodeURIComponent(pValue);
                } else {
                    params = params + "&" + pName + "=" + encodeURIComponent(pValue);
                }
            }
            if (document.getElementById("selection") == null && (pName == 'filterChecked' || pName == 'ml' || pName == 'mp' || pName == 'md' || pName == 'me')) {
                params = params + "&" + pName + "=" + encodeURIComponent(pValue);
            }
        }
    }
    if(id == "reportLink" || id == "reportsLink") {
        newHref = s1+params;
    } else {
        newHref = s1+params;
    }
    if(document.getElementById("selection") == null){
        document.getElementById(id).href = newHref;
    } else {
        if(document.getElementById("selection").checked){
            document.getElementById(id).href = newHref + createMoreLessParamString() + "&filterChecked=true" ;
        } else {
            document.getElementById(id).href = s1 + createMoreLessParamString() + "&filterChecked=false";
        }
    }
}
