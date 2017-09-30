/**
 * Created by root on 9/19/17.
 */
'use strict';

$(document).ready(function () {
    $("#shl-item, #shl-price").addClass('text-center');
    $(".shl-input").addClass('text-center');
    $("#username, #password, #email, #password, #confirm, #name").addClass('form-control');
    $('#item_name').addClass('form-control').attr('placeholder', 'Item name');
    $('#quantity').addClass('form-control').attr('placeholder', 'Quantity');
    $('#price').addClass('form-control').attr('placeholder', 'Price per quantity');
    $('#email').addClass('form-control').attr('placeholder', 'Email');
    $('#confirm').addClass('form-control').attr('placeholder', 'Confirm Password');
    $('#name').addClass('form-control').attr('placeholder', 'Shopping list name');
    $('form ul').addClass('list-unstyled');
    $('form ul li').addClass('form-error');
    $('li.form-error').addClass('text-danger');
});



document.getElementById('username').placeholder = 'Username';
document.getElementById('password').placeholder = 'Password';