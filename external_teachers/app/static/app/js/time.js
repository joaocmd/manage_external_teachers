function getMoment(dateString) {
	var lastweek = moment().subtract('days',7);
	var date = moment(dateString, 'DD/MM/YYYY HH:mm');

	if(date.isBefore(lastweek)) {
        return dateString;
    } else {
        return date.fromNow();
    }
}

$(function() {
	//Iterate all over the elements with a date and put it right
	$('[data-date]').each(function() {
		var date = getMoment($(this).attr('data-date'));
		$(this).text(date);
	});

});
