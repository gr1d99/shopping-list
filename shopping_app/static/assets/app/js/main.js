/**
 * Created by root on 9/19/17.
 */
'use strict';

$(document).ready(function () {
    $("#shl-item, #shl-price").addClass('text-center');
    $(".shl-input").addClass('text-center');
    $("#username, #password").addClass('form-control');
});

document.getElementById('username').placeholder = 'Username';
document.getElementById('password').placeholder = 'Password';