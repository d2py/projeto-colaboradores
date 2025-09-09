from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator




FERIAS=(
    ('JAN', "Janeiro"),
    ('FEV', "Fevereiro"),
    ('MAR', "Março"),
    ('ABR', "ABRIL"),
    ('MAI', "MAIO"),
    ('JUN', "Junho"),
    ('JUL', "Julho"),
    ('AGO', "Agosto"),
    ('SET', "Setembro"),
    ('OUT', "Outubro"),
    ('NOV', "Novembro"),
    ('DEZ', "Desembro"),
)

STATUS = (
    ('SIM', "Banheirista"),
    ('NAO', "Não Banheirista")
)

TAMANHO_ROUPA=(
    ("P", "P"),
    ("M", "M"),
    ("G", "G"),
    ("GG", "GG"),
    ("EXTRAG", "EXTRA GG")   
)

TAMANHO_CALCADO=(
    (34, "34"),
    (35, "35"),
    (36, "36"),
    (37, "37"),
    (38, "38"),
    (39, "39"),
    (40, "40"),
    (41, "41"),
    (42, "42"),
    (43, "43"),
    (44, "44"),
    (45, "45")
)

class Funcionario(models.Model):
    matricula_funcionario = models.PositiveIntegerField(primary_key=True, max_length=6)
    nome_funcionario = models.CharField(max_length=60,verbose_name="Nome Funcionario",blank=False , validators=[ RegexValidator(
        r'^[a-zA-ZáàâãéèêióôõúçñÁÀÂÃÉÈÊIÓÔÕÚÇÑ\s]+$',
        'Apenas letras são permitido no nome.'
    )])
    status = models.CharField(choices=STATUS, verbose_name="Status" ,max_length=3, null=False, default="NAO")
    ferias = models.CharField(choices=FERIAS,verbose_name="Ferias" ,max_length=3,blank=True , null=True )

    def __str__(self):
        return self.nome_funcionario

class Uniformes(models.Model):
    calca = models.CharField(choices=TAMANHO_ROUPA, max_length=6, verbose_name="Calça", null=False, blank=False)
    blusa = models.CharField(choices=TAMANHO_ROUPA, max_length=6, verbose_name="Blusa", null=False, blank=False)
    blusa_frio = models.CharField(choices=TAMANHO_ROUPA, max_length=6, verbose_name="Blusa de Frio", null=False, blank=False)
    sapato = models.PositiveSmallIntegerField(choices=TAMANHO_CALCADO,  verbose_name="Sapato",null=False, blank=False,validators=[
        MinValueValidator(34),
        MaxValueValidator(45)
    ])
    galocha = models.PositiveSmallIntegerField(choices=TAMANHO_CALCADO, validators=[
        MinValueValidator(34),
        MaxValueValidator(45)
    ],null=False, blank=False)
    matricula_funcionario_id = models.OneToOneField(Funcionario,null=True,blank=False , on_delete=models.CASCADE, related_name='uniformes')


class Setores(models.Model):
    setor = models.CharField(max_length=40, verbose_name='Setores',null=False, unique=True,   validators=[ RegexValidator(
        r'^[a-zA-Z0-9áàâãéèêióôõúçñÁÀÂÃÉÈÊIÓÔÕÚÇÑ\s]+$',
        'Apenas letras são permitido no nome.'
    )])
    def save(self, *args, **kwargs):
        self.setor = self.setor.upper()
        super().save(*args, **kwargs)

    matricula_funcionario = models.ForeignKey(Funcionario,null=True,blank=True ,on_delete=models.SET_NULL,related_name='setores')
    
    def __str__(self):
        return self.setor