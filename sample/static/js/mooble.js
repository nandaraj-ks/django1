function compareDates(start, end, convert) {
    if (convert) {
        start = getDateFromString(start);
        end = getDateFromString(end);
    }
    result = start - end;
    return result;
}

function getFormattedDate(jsDateObj) {
    var day = jsDateObj.getDate();
    var month = jsDateObj.getMonth() + 1;
    var year = jsDateObj.getFullYear();
    return (day < 10 ? '0' + day : day) + '/' + (month < 10 ? '0' + month : month) + '/' + year;
}

function getDateFromString(dateString) {
    var dateSplit = dateString.split('/');
    var day = parseInt(dateSplit[0]);
    var month = parseInt(dateSplit[1]) - 1; // since javascript Date month is zero indexed.
    var year = parseInt(dateSplit[2]);
    return new Date(year, month, day);
}

function setFormFieldValues(jsonObj, formId) {
    $.each($('#' + formId + ' :input').not(':input[type=button], :input[type=submit], :input[type=reset]'), function(index, element) {
        $(element).val(jsonObj[$(element).attr('name')]);
    });
    $.each($('#' + formId + ' select'), function(index, element) {
        $(element).val(jsonObj[$(element).attr('name')]);
    });
}

function showFormErrors(jsonObj, formId) {
    $.each($('#' + formId + ' span.error'), function (index, element) {
        if (jsonObj[$(element).attr('name')]) {
            $(element).text(jsonObj[$(element).attr('name')][0]);
        }
    });
}

function clearFormErrors(formId) {
    $.each($('#' + formId + ' span.error'), function (index, element) {
        $(element).text('');
    });
}

function clearFormFieldValues(formElement, notClearClass) {
    $.each($('#' + formElement + ' :input').not(':input[type=button], :input[type=submit], :input[type=reset], .' + notClearClass), function(index, element) {
        if ($(element).is(':checkbox') || $(element).is(':radio')) {
            $(element).prop('checked', '');
        } else {
            $(element).val('');
        }
    });
}

function populateTemplate(container, tmplt, values) {
    $('#' + container).loadTemplate($('#' + tmplt), values);
}

function showSettingsTab(tab) {
    $.each($('.customTabs ul.nav-tabs li'), function (index, elem) {
        $(elem).removeClass('active');
    });
    $.each($('div.tabContents'), function(index, elem) {
        $(elem).hide();
    });
    switch (tab) {
        case 0: $('#tab0').addClass('active');
                $('#myAccountTabContent').slideDown(800);
                break;
        case 1: $('#tab1').addClass('active');
                $('#deviceTabContent').slideDown(800);
                break;
        case 2: break;
        case 3: $('#tab3').addClass('active');
                $('#manageUserTabContent').slideDown(800);
                showUserList();
                break;
    }
}

function showUserList() {
    var ajaxRequest = $.ajax({
        'url' : "/employee/ajaxCall/getUsers",
        'data' : {arg : JSON.stringify([])},
        'type' : 'POST',
        'dataType' : 'json',
        // by default async is true, this is FYI
        'async' : true
    });
    // callback handler that will be called on success
    ajaxRequest.done(function(response) {
        console.log(response);
    });
    // callback handler that will be called on failure
    ajaxRequest.fail(function (error){
        // log the error to the console
        console.error("The following error occured: "+ error);
    });
}