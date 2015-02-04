jQuery.noConflict();

(function($) {

$(document).ready(function() {
    // Use jQuery via $j(...)
    var $j = jQuery.noConflict();
    var ifExists = "true";
    $j(document).ready(function(){
        try{
            $j("#codeLocHash").select2();
        }
    catch(err)
    {
        ifExists = "false";
    }    
    });
    
        $j(document).ready(function() {
                var snippetResultSize= $('#resultSize').text();
                for(var k=1;k<=snippetResultSize;k++){
                    try{
                        $j("#codeLocHash"+k).select2();
                    }
                    catch(err){
                        ifExists = "false";
                    }   
                }
        });
    
// Global Elements
var snippetResultSize= $('#resultSize').text();
var $header = $('#header');
var header_height = $header.outerHeight(true);

var $footer = $('#footer');
var footer_height = $footer.outerHeight(true);

var $ohlohfooter = $('#ohlohfooter');
var ohlohFooter_height = $ohlohfooter.outerHeight(true);

var $file_view_header = $('div.file_view_header');
var file_view_header_height = $file_view_header.outerHeight(true);

//Landing Page Elements
var $landing_page_frame = $('#landing_page_frame');
var landing_page_frame_height = $landing_page_frame.outerHeight(true);
//var $example_searches = $('#example_searches');

var $header_page_frame = $('#header_page_frame');

var $column_left = $('div.column_left');

var    $project_info =$('div.project_info');
var project_info_height = $project_info.outerHeight(true);

var class_header_height = $('div.class_viewer').children('.column_header').outerHeight(true);

var project_header_height = $('div.project_page_left').children('.column_header').outerHeight(true);

var $class_viewer = $('div.class_viewer');
var class_viewer_height = $($class_viewer).outerHeight(true);

var $classViewerPanel = $('#classViewerPanel');

var $projectViewerPanel = $('#projectViewerPanel');

//var project_header_height = $('div.project_viewer').children('.column_header').outerHeight(true);
var $project_viewer = $('div.project_viewer');
var project_viewer_height = $project_viewer.outerHeight(true);

var $file_view_body = $('div.file_view_body');

var $file_view_column = $('div.file_view_column');

var $single_folder_viewer = $('div.single_folder_viewer');
var single_folder_viewer_height = $('div.single_folder_viewer').outerHeight(true);

var code_header_height = $('div.column_right_wide').children('.column_header').outerHeight(true);
var project_page_left_height = $('#project_page_left').children('.column_header').outerHeight(true);

var $code_parent = $('div.code_parent');
var $filesInFolder =  $('div.filesInFolder');
var $code_line_num = $('pre.code_line_num');

var $code_view = $('pre.code_view');

var $file_list = $('div.file_list');

var $project_list = $('div.project_list');

var $code_view_options = $('ul.code_view_options');

var exp_header_height = $('div.single_folder_viewer div.exp_header').outerHeight(true);

var snippetResultsContainerHead_height = $('#snippetResultsContainerHead').outerHeight(true);



var $search_results = $('div.search_results');

var $search_scroll = $('div.search_scroll');

var $error_scroll = $('div.error_scroll');

var $search_filters = $('#search_filters');

var $snippet_results_pagination = $('#snippet_results_pagination');
var snippet_results_pagination_height = $($snippet_results_pagination).outerHeight(true);

// Set File View layout 
//$($file_view_header).css({'top':header_height+'px'});
//$($file_view_body).css({'top':header_height+file_view_header_height+'px'});
//$($code_view_options).css({'top':header_height+file_view_header_height-1+'px'});

//Project Page Elements

var $project_name = $('#breadcrumbs');

//var $table_top = $('#table_top');

var $filesInFolder = $('#filesInFolder');

var $project_table = $('#ohlohproject_table');

var $sidebar_scoller = $('#sidebar_scoller');

var project_sidebar_title_height = $('#project_sidebar_title').outerHeight(true);

var win_width = $(window).width();

//Adding Project Description On Ohloh Project View Page
var $projectDesc = $('#projectDesc');
var $moreDesc = $('#more_desc');
var project_name_height = $project_name.outerHeight(true);
var $project_description_content = $('#project_description_content');
var project_description_content_text = $project_description_content.text();

if(win_width <1000){
    //alert(project_description_content_text.length);
    if (project_description_content_text.length > 550) {
        //alert(project_description_content_text.length);
        $($projectDesc).css({'height':"60px"});
     var project_blurb = project_description_content_text.substring(0, 550);
     $project_description_content.text(project_blurb+' ').append('<span class="triangleColor">&#x25B6;</span><a id="more_info" class="tileSmallLink">More</a>');
     
     
     function popFrame() {
     var win_width = $(window).width();
     var win_height = $(window).height();
     
     $('#project_description_content').text('');
     $('#more_desc').text(project_description_content_text).append('<span class="triangleColor">&#x25B2;<span><a id="less_info" class="tileSmallLink">Less</a>');
     $($moreDesc).css({'border':"1px solid #CCC"});
     //$('#project_description_content').text(project_description_content_text).append('<span class="triangleColor">&#x25B2;<span><a id="less_info" class="tileSmallLink">Less</a>');
     //$('#project_description_content').height((win_height*.8)-header_height-footer_height-project_name_height);
     $('#less_info').click(lessFrame);
     }

     function lessFrame() {
         var win_width = $(window).width();
         var win_height = $(window).height();
//         var $pop_frame = $('#pop_frame');     
//         $pop_frame.css({ 'left':(win_width-500)/2, 'top':(win_height*.1) }).css({'max-height':(win_height*.8)}).fadeIn();
         //$('#project_description_content').text(project_blurb+' ').append('<span class="triangleColor">&#x25B6;<span><a id="more_info1" class="tileSmallLink">More</a>');
         $('#project_description_content').text(project_blurb+' ').append('<span class="triangleColor">&#x25B6;<span><a id="more_info1" class="tileSmallLink">More</a>');
         $('#more_desc').text('');
         $($moreDesc).css({'border':"none"});
         //$('#project_description_content').height((win_height*.8)-header_height-footer_height-project_name_height);
         $('#more_info1').click(popFrame);
     }
     
     $('#more_info').click(popFrame);
     
    }else if (project_description_content_text.length > 0 &&  project_description_content_text.length <= 280){
        $($projectDesc).css({'height':"20px"});
    }else if (project_description_content_text.length > 280 && project_description_content_text.length <= 160  ){
        $($projectDesc).css({'height':"40px"});
    }else if (project_description_content_text.length > 360 && project_description_content_text.length < 471  ){
        $($projectDesc).css({'height':"60px"});
    }
    }
else if(win_width >=1000 && win_width < 1280){
    if (project_description_content_text.length > 520) {
        $($projectDesc).css({'height':"60px"});
     var project_blurb = project_description_content_text.substring(0, 520);
     $project_description_content.text(project_blurb+' ').append('<span class="triangleColor">&#x25B6;</span><a id="more_info" class="tileSmallLink">More</a>');
     
     
     function popFrame() {
     var win_width = $(window).width();
     var win_height = $(window).height();
     
     $('#project_description_content').text('');
     $('#more_desc').text(project_description_content_text).append('<span class="triangleColor">&#x25B2;<span><a id="less_info" class="tileSmallLink">Less</a>');
     $($moreDesc).css({'border':"1px solid #CCC"});
     //$('#project_description_content').text(project_description_content_text).append('<span class="triangleColor">&#x25B2;<span><a id="less_info" class="tileSmallLink">Less</a>');
     //$('#project_description_content').height((win_height*.8)-header_height-footer_height-project_name_height);
     $('#less_info').click(lessFrame);
     }

     function lessFrame() {
         var win_width = $(window).width();
         var win_height = $(window).height();
//         var $pop_frame = $('#pop_frame');     
//         $pop_frame.css({ 'left':(win_width-500)/2, 'top':(win_height*.1) }).css({'max-height':(win_height*.8)}).fadeIn();
         //$('#project_description_content').text(project_blurb+' ').append('<span class="triangleColor">&#x25B6;<span><a id="more_info1" class="tileSmallLink">More</a>');
         $('#project_description_content').text(project_blurb+' ').append('<span class="triangleColor">&#x25B6;<span><a id="more_info1" class="tileSmallLink">More</a>');
         $('#more_desc').text('');
         $($moreDesc).css({'border':"none"});
         //$('#project_description_content').height((win_height*.8)-header_height-footer_height-project_name_height);
         $('#more_info1').click(popFrame);
     }
     
     $('#more_info').click(popFrame);
     
    }else if (project_description_content_text.length > 0 &&  project_description_content_text.length <= 375){
        $($projectDesc).css({'height':"20px"});
    }else if (project_description_content_text.length > 375 && project_description_content_text.length <= 550  ){
        $($projectDesc).css({'height':"40px"});
    }else if (project_description_content_text.length > 550 && project_description_content_text.length < 671  ){
        $($projectDesc).css({'height':"60px"});
    }
    }
else if(win_width >=1280 && win_width < 1360){
if (project_description_content_text.length > 650) {
    $($projectDesc).css({'height':"60px"});
 var project_blurb = project_description_content_text.substring(0, 650);
 $project_description_content.text(project_blurb+' ').append('<span class="triangleColor">&#x25B6;</span><a id="more_info" class="tileSmallLink">More</a>');
 
 
 function popFrame() {
 var win_width = $(window).width();
 var win_height = $(window).height();
 
 $('#project_description_content').text('');
 $('#more_desc').text(project_description_content_text).append('<span class="triangleColor">&#x25B2;<span><a id="less_info" class="tileSmallLink">Less</a>');
 $($moreDesc).css({'border':"1px solid #CCC"});
 //$('#project_description_content').text(project_description_content_text).append('<span class="triangleColor">&#x25B2;<span><a id="less_info" class="tileSmallLink">Less</a>');
 //$('#project_description_content').height((win_height*.8)-header_height-footer_height-project_name_height);
 $('#less_info').click(lessFrame);
 }

 function lessFrame() {
     var win_width = $(window).width();
     var win_height = $(window).height();
//     var $pop_frame = $('#pop_frame');     
//     $pop_frame.css({ 'left':(win_width-500)/2, 'top':(win_height*.1) }).css({'max-height':(win_height*.8)}).fadeIn();
     //$('#project_description_content').text(project_blurb+' ').append('<span class="triangleColor">&#x25B6;<span><a id="more_info1" class="tileSmallLink">More</a>');
     $('#project_description_content').text(project_blurb+' ').append('<span class="triangleColor">&#x25B6;<span><a id="more_info1" class="tileSmallLink">More</a>');
     $('#more_desc').text('');
     $($moreDesc).css({'border':"none"});
     //$('#project_description_content').height((win_height*.8)-header_height-footer_height-project_name_height);
     $('#more_info1').click(popFrame);
 }
 
 $('#more_info').click(popFrame);
 
}else if (project_description_content_text.length > 0 &&  project_description_content_text.length <= 375){
    $($projectDesc).css({'height':"20px"});
}else if (project_description_content_text.length > 375 && project_description_content_text.length <= 550  ){
    $($projectDesc).css({'height':"40px"});
}else if (project_description_content_text.length > 550 && project_description_content_text.length < 671  ){
    $($projectDesc).css({'height':"60px"});
}
}else if(win_width >=1360){
    if (project_description_content_text.length > 705) {
        $($projectDesc).css({'height':"60px"});
     var project_blurb = project_description_content_text.substring(0, 705);
     $project_description_content.text(project_blurb+' ').append('<span class="triangleColor">&#x25B6;</span><a id="more_info" class="tileSmallLink">More</a>');
     
     
     function popFrame() {
     var win_width = $(window).width();
     var win_height = $(window).height();
     
     $('#project_description_content').text('');
     $('#more_desc').text(project_description_content_text).append('<span class="triangleColor">&#x25B2;<span><a id="less_info" class="tileSmallLink">Less</a>');
     $($moreDesc).css({'border':"1px solid #CCC"});
     //$('#project_description_content').text(project_description_content_text).append('<span class="triangleColor">&#x25B2;<span><a id="less_info" class="tileSmallLink">Less</a>');
     //$('#project_description_content').height((win_height*.8)-header_height-footer_height-project_name_height);
     $('#less_info').click(lessFrame);
     }

     function lessFrame() {
         var win_width = $(window).width();
         var win_height = $(window).height();
//         var $pop_frame = $('#pop_frame');     
//         $pop_frame.css({ 'left':(win_width-500)/2, 'top':(win_height*.1) }).css({'max-height':(win_height*.8)}).fadeIn();
         //$('#project_description_content').text(project_blurb+' ').append('<span class="triangleColor">&#x25B6;<span><a id="more_info1" class="tileSmallLink">More</a>');
         $('#project_description_content').text(project_blurb+' ').append('<span class="triangleColor">&#x25B6;<span><a id="more_info1" class="tileSmallLink">More</a>');
         $('#more_desc').text('');
         $($moreDesc).css({'border':"none"});
         //$('#project_description_content').height((win_height*.8)-header_height-footer_height-project_name_height);
         $('#more_info1').click(popFrame);
     }
     
     $('#more_info').click(popFrame);
     
    }else if (project_description_content_text.length > 0 &&  project_description_content_text.length <= 375){
        $($projectDesc).css({'height':"20px"});
    }else if (project_description_content_text.length > 375 && project_description_content_text.length <= 550  ){
        $($projectDesc).css({'height':"40px"});
    }else if (project_description_content_text.length > 550 && project_description_content_text.length < 671  ){
        $($projectDesc).css({'height':"60px"});
    }
    }

//Add 1st and last child classes to specific elements.  This should be made more universal.
$('#example_searches').children('div:first-child').addClass('first_child');
$('#example_searches').children('div:last-child').addClass('last_child');

$('ul.code_view_options li:first-child').addClass('first_child');
$('div.snippetResult').first().addClass('first_child');

$file_list.children().first().addClass('first_child');
$file_list.children().last().addClass('last_child');

$classViewerPanel.children().first().addClass('first_child');
$classViewerPanel.children().last().addClass('last_child');

$('div.login_links a:last-child, div.crumb_category span:last-child, ul.code_view_options li:last-child').addClass('last_child');
$('div.exp_header').first().addClass('first_child');

$('#share_link').children('div:first-child').addClass('tweet');
$('#share_link').children('div:last-child').addClass('searchOnGoogle');


//Temp remove Search Results Right Column if Project Results is 0

var $project_results = $('div.project_results');
if(    ($project_results).length == 0) 
{ 
$($search_results).addClass('search_results_wide1'); 
}

//IQ for landing page search box
var $search_field = $landing_page_frame.find('input:first');
$search_field.val('Search open source code').focus();
$search_field.click(function() {
var entered_text = $search_field.val();
if ( (entered_text == 'Search open source code')) {
$search_field.val('');
$(this).attr('placeholder','');
}
});
$search_field.blur(function() {
var entered_text = $search_field.val();
if (entered_text == '') {
$search_field.val('Search open source code');
$(this).attr('placeholder','Search open source code');
}
});
$('#landing_page_form').submit(function(event) {
    //clearing the cookie set for remembering codeFilter scroller position 
     var strCook = document.cookie;
     var strCookie;
     if(strCook.indexOf("!~")!=0){
         var intS = strCook.indexOf("!~");
         var intE = strCook.indexOf("~!");
         var strPos = strCook.substring(intS+2,intE);
         strCookie = "yPos=!~" + strPos + "~!";      
         document.cookie = strCookie + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
    //end cookie cleared
var entered_text = $search_field.val();
if ( (entered_text == 'Search open source code')) {
event.preventDefault();
$search_field.val('');
}
});

$search_field.keydown(function() {
    var entered_text = $search_field.val();
    entered_text = jQuery.trim(entered_text);
    if ((entered_text == 'Search open source code')) {
        $search_field.val('');
        $(this).attr('placeholder','');
    }
    });


//IQ for Header Page Search Box
var $header_search_field = $header_page_frame.find('input:first');
$header_search_field.click(function() {
var entered_text = $header_search_field.val();
if ( (entered_text == 'Search open source code')) {
$header_search_field.val('');
$(this).attr('placeholder','');
}
});
$header_search_field.blur(function() {
var entered_text = $header_search_field.val();
if (entered_text == '') {
    $header_search_field.val('Search open source code');
$(this).attr('placeholder','Search open source code');
}
});
$('#searchForm').submit(function(event) {
    //clearing the cookie set for remembering codeFilter scroller position 
     var strCook = document.cookie;
     var strCookie;
     if(strCook.indexOf("!~")!=0){
         var intS = strCook.indexOf("!~");
         var intE = strCook.indexOf("~!");
         var strPos = strCook.substring(intS+2,intE);
         strCookie = "yPos=!~" + strPos + "~!";      
         document.cookie = strCookie + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
    //end cookie cleared
var entered_text = $header_search_field.val();
if ( (entered_text == 'Search open source code')) {
event.preventDefault();
$header_search_field.val('');
}
});

$header_search_field.keydown(function() {
    var entered_text = $header_search_field.val();
    entered_text = jQuery.trim(entered_text);
    if ((entered_text == 'Search open source code')) {
        $header_search_field.val('');
        $(this).attr('placeholder','');
    }
    });

$('#example_search_toggle').toggle(

function() {
    $(this).html('&#x25BC; Hide search examples');
    $('#example_searches').slideDown();
},

function() {
    $(this).html('&#x25B6; Show search examples');
    $('#example_searches').slideUp();
}
);


//share link
$('#share_link_toggle').click(function()
        {
    if ($('#share_link').is(':hidden')){
        $('#share_link').slideDown();
    }
    else{
        $('#share_link').slideUp();
    }
});

$("body").click(function() {
    $('#share_link').hide();
});

$('#share_link_toggle').click(function(e) {
    e.stopPropagation();
});

//End


File_View_Layout();
function File_View_Layout() {
var win_height = $(window).height();
var middle_space = win_height-header_height-project_info_height-code_header_height-footer_height-66;
if ($classViewerPanel.length == 0) {
$file_list.css({'height':(middle_space)+"px"});
}
else {
var class_header_height = $('div.class_viewer').children('.column_header').outerHeight(true);
$classViewerPanel.height((middle_space/2)-class_header_height+10);
var class_viewer_height = $($class_viewer).outerHeight(true);
$file_list.height(middle_space-class_viewer_height);
}
$code_parent.height(middle_space);
$code_parent.find('#code_line_num').css({'min-height':middle_space-1+"px"});
}


//////////

var $last_row = $project_table.find('tr:last-child');
$last_row.find('td').addClass('last_row');
$last_row.find('td').first().addClass('first');
$last_row.find('td').last().addClass('last');


//////////

Search_Results_Layout();
function Search_Results_Layout() {
var win_height = $(window).height();
var keepCurrentFilters_height = $('div.keepCurrentFilters').outerHeight(true);
var middle_space = win_height-header_height-snippetResultsContainerHead_height-keepCurrentFilters_height-footer_height-65;
var search_middle_space = win_height-header_height-snippetResultsContainerHead_height-footer_height-65;
var error_middle_space = win_height-header_height-snippetResultsContainerHead_height-footer_height-65;
$($search_scroll).css({'height':middle_space+"px"});
$($search_filters).css({'height':search_middle_space+"px"});
$($error_scroll).css({'height':error_middle_space+"px"});
if($code_parent.height()==null){
$('#ohfooter').css({'padding-bottom':"54px"});
}
}

$(window).resize(function() {
File_View_Layout(); 
Search_Results_Layout();
//Example_Search_Layout();
Project_Detail_Layout();
});

//////////Layout for the Project Detail Page
Project_Detail_Layout();
function Project_Detail_Layout() {
var win_height = $(window).height();
var ohlohproject_desc_height = $projectDesc.outerHeight(true);
var middle_space = win_height-ohlohproject_desc_height-header_height-project_info_height-project_page_left_height-footer_height-102;
var project_header_height = $('div.project_viewer').children('.future_header').outerHeight(true);
if(project_header_height == null){
    $('#project_page_left').css({'margin-right':"20px"});
}
$projectViewerPanel.height(middle_space-project_header_height-262);

//$project_list.height(middle_space-project_viewer_height+10);
$filesInFolder.height(middle_space);
}


////Example_Search_Layout();
/*
function Example_Search_Layout(){
    var exampleHeight=landing_page_frame_height-313;
    var win_height = $(window).height();
    //alert(exampleHeight+"landing_page_frame_height=="+landing_page_frame_height+"win_height"+win_height);
    
    //$example_searches.outerHeight(landing_page_frame_height-310);
    if(win_height<650){
        //alert("set acrolle");
        $($example_searches).css({'overflow':"auto"});
        $($example_searches).css({'overflow-x':"hidden"});
        $($example_searches).css({'height': exampleHeight});
        
    }else{
        $($example_searches).css({'overflow':"none"});
        $($example_searches).css({'height': ""});
        
    }
    $($example_searches).css({'max-width': "none"});
    
    
}
*/
// Scroll line # column into view with ling x scrolls
/*
function scrollPos() {
var scrollY = $(cv).scrollTop();
$(cln).css({'top':-scrollY+'px'});
}



$(cv).scroll(function() {
scrollPos();
});
*/

//Submit button hover change
/*
$('#searchForm input.submit').hover(function() {
    $(this).addClass('grey_shade_vert2');
},
function() {
    $(this).removeClass('grey_shade_vert2');
});
*/

//Show code view styles
$('a.editor_style_button').toggle(function(e) {
    
    $(this).text('Hide Editor Styles').addClass('grey_shade_vert2');
    $('.code_view_options').slideDown(300);
    event.preventDefault();
},
function() {
    $(this).text('Show Editor Styles').removeClass('grey_shade_vert2');
    $('.code_view_options').slideUp(300);
    event.preventDefault();
});

$("#classViewerPanel").jstree({  
     "core" : { "initially_open" : [ "rootNode"], "animation" : 100 },         
    "themes": { "theme": "classic",   "dots":false,  "icons": false },
    "plugins" : [ "themes", "html_data" ]
     });


//Fix Line number X position
/*
var clnXY = $(cln).offset();

$(cln).css({'position':'fixed', 
            'top':clnXY.top+'px', 
            'left':clnXY.left+'px'
            });
$('.temp_place_holder').text('<p>'+clnXY.top+'</p><p>'+clnXY.left+'</p>');

*/

/*

$($project_info).click(function() {
var win_height = $(window).outerHeight();
var win_width = $(window).outerWidth();
var project_text = $($project_info).text();
$('<p>'+project_text+'</p>').prependTo('#popup');
$('#popup').css({'left':(win_width-800)/2+'px', 'top':(win_height-500)/2+'px'}).fadeIn(300);
$('#overlay').fadeIn(300);
});

$('#popup').click(function() {
$('#popup').fadeOut(300);
$('#overlay').fadeOut(300);
});

*/


for(var i=1;i<=snippetResultSize;i++){
    var check = $("#codeLocHash"+i);
    var r=i;
    
    
    $("#codeLocHash"+i+" option").each(function() { 
           //alert($(this).val()); //do something with this text
           var hideall = "#"+"f"+i+"filePath"+$(this).val();
           var hideAllFile="#"+"n"+i+"fileName"+$(this).val();
           var hideAllProj="#"+"p"+i+"projName"+$(this).val();  
           $(hideall).css({'display':'none'});
           $(hideAllFile).css({'display':'none'});
           $(hideAllProj).css({'display':'none'});
           
        });

        var toshow="#"+"f"+i+"filePath"+check.val();
        $(toshow).css({'display':'block'});
        
        var toshowFile="#"+"n"+i+"fileName"+check.val();
        $(toshowFile).css({'display':'block'});
        
        var toshowProj="#"+"p"+i+"projName"+check.val();
        $(toshowProj).css({'display':'block'});
        
        //$(toshow).children().show();
        
        

$("#codeLocHash"+i).change(function() { 
    var cid = $(this).attr('id');
    var codeLocId = $(this).val(); 
    var toRemove = 'codeLocHash';
    var id = cid.replace(toRemove,'');
    $("#"+$(this).attr('id')+" option").each(function() { 
        

            var hideOnChangeId ="#"+id+"hide"+$(this).val();
            if($(hideOnChangeId).hasClass('show')){
                $(hideOnChangeId).removeClass('show').addClass('hide');
            }
            
            var showMoreId="#"+"more"+id+$(this).val();
            if($(showMoreId).hasClass('hide')){
                $(showMoreId).removeClass('hide').addClass('show');
            }
            
            var showLessId="#"+"less"+id+$(this).val();
            if($(showLessId).hasClass('show')){
                $(showLessId).removeClass('show').addClass('hide');
            }
           var hide = "#"+"f"+id+"filePath"+$(this).val();
           $(hide).css({'display':'none'});
           
           var hideFile = "#"+"n"+id+"fileName"+$(this).val();
           $(hideFile).css({'display':'none'});
           
           var hideProj = "#"+"p"+id+"projName"+$(this).val();
           $(hideProj).css({'display':'none'});
           
        });
    var toshow = "#"+"f"+id+"filePath"+codeLocId;
    $(toshow).css({'display':'block'});
    
    var toshowFile = "#"+"n"+id+"fileName"+codeLocId;
    $(toshowFile).css({'display':'block'});
    
    var toshowProj = "#"+"p"+id+"projName"+codeLocId;
    $(toshowProj).css({'display':'block'});
    });
}


}); // END $(document).ready(function()


})(jQuery);