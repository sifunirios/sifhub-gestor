from django.core import validators


class RegistryValidator(validators.RegexValidator):
    regex = r'^\d{3}\.\d{2}\.\d{3}$'
    message = (
        'Informe uma matrícula válida com 8 números separados por '
        'pontos. Ex: 162.20.035.'
    )


class AcademicYearValidator(validators.RegexValidator):
    regex = r'^\d{4}\.\d{1}$'
    message = 'Informe o ano e o período letivo separados por ponto. Ex: 2017.1.'
