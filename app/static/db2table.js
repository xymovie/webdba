//timer id
var refreshTimer;

function setRefreshTimer(t) {
	t = t || 2000;
	refreshTimer = setInterval(function() {
	    rex = search();
	    populate(rex);
	}, t);
}

function disableRefresh() {
	if (!refreshTimer) {
		clearInterval(refreshTimer);
		refreshTimer = null;
	}
}


$(document).ready(function(){
   var rex;
   function search (){
        $('#filter').keyup(function () {
            rex = new RegExp($(this).val(), 'i');
            $('.searchable tr').hide();
            $('.searchable tr').filter(function () {
                return rex.test($(this).text());
            }).show();

        })

        return rex;
    }

   function populate(rex) {
       $.ajax({
           url: $SCRIPT_ROOT + "/db2/entries",
           cache: false, 
           success: function(html) {
               $(".refresh").html(html);
               if (rex) {
                   $('.searchable tr').hide();
                   $('.searchable tr').filter(function () {
                       return rex.test($(this).text());
                       }).show();
               }
           }
       });
   }
   populate(rex);
   setRefreshTimer();
});

