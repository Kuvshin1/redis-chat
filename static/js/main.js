(function ($) {
    "use strict";


    /*==================================================================
    [ Focus input ]*/
    $('.input100').each(function () {
        $(this).on('blur', function () {
            if ($(this).val().trim() != "") {
                $(this).addClass('has-val');
            }
            else {
                $(this).removeClass('has-val');
            }
        })
    })


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit', function () {
        var check = true;

        for (var i = 0; i < input.length; i++) {
            if (validate(input[i]) == false) {
                showValidate(input[i]);
                check = false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function () {
        $(this).focus(function () {
            hideValidate(this);
        });
    });

    function validate(input) {
        return true;
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }

    /*==================================================================
    [ Show pass ]*/
    var showPass = 0;
    $('.btn-show-pass').on('click', function () {
        if (showPass == 0) {
            $(this).next('input').attr('type', 'text');
            $(this).find('i').removeClass('zmdi-eye');
            $(this).find('i').addClass('zmdi-eye-off');
            showPass = 1;
        }
        else {
            $(this).next('input').attr('type', 'password');
            $(this).find('i').addClass('zmdi-eye');
            $(this).find('i').removeClass('zmdi-eye-off');
            showPass = 0;
        }

    });
    /*==================================================================
    [ Sing in or up ]*/
    var signIn = 1;
    $('#0').on('click', function () {
        if (signIn == 0) {
            $('#0').addClass('active-auth')
            $('#1').removeClass('active-auth')
            $('.wrap-login100-form-btn .login100-form-btn').html('Login')
            $('[data-validate="retry password"]').css('display', 'none');
            signIn = 1;
        }
    });

    $('#1').on('click', function () {
        if (signIn == 1) {
            $('#1').addClass('active-auth')
            $('#0').removeClass('active-auth')
            $('.wrap-login100-form-btn .login100-form-btn').html('Create account')
            $('[data-validate="retry password"]').css('display', 'block');
            signIn = 0;
        }
    });


    function showModal() {
        $('#connectToChat').css('display', 'block');
    }

})(jQuery);