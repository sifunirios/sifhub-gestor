django.jQuery($ => {
    // accounts.Client
    $('#id_business-0-cnpj').mask('00.000.000/0000-00');
    $('#id_business-0-telephone').mask('(00) 00000-0000');

    // accounts.Member
    $('#id_profile-0-registry').mask('000.00.000');
    $('#id_profile-0-initial_academic_year').mask('0000.0');
});
