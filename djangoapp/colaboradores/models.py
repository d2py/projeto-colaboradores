from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


# ─────────────────────────────────────────────
#  USUÁRIO CUSTOMIZADO
# ─────────────────────────────────────────────

class CustomUser(AbstractUser):
    PREPOSTA     = 'preposta'
    ENCARREGADA  = 'encarregada'

    ROLE_CHOICES = [
        (PREPOSTA,    'Preposta'),
        (ENCARREGADA, 'Encarregada'),
    ]

    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES,
        default=ENCARREGADA,
        verbose_name='Perfil',
    )

    @property
    def is_preposta(self):
        return self.role == self.PREPOSTA

    @property
    def is_encarregada(self):
        return self.role == self.ENCARREGADA

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'


# ─────────────────────────────────────────────
#  CHOICES
# ─────────────────────────────────────────────

FERIAS = (
    ('JAN', 'Janeiro'),
    ('FEV', 'Fevereiro'),
    ('MAR', 'Março'),
    ('ABR', 'ABRIL'),
    ('MAI', 'MAIO'),
    ('JUN', 'Junho'),
    ('JUL', 'Julho'),
    ('AGO', 'Agosto'),
    ('SET', 'Setembro'),
    ('OUT', 'Outubro'),
    ('NOV', 'Novembro'),
    ('DEZ', 'Desembro'),
)

STATUS = (
    ('SIM', 'Banheirista'),
    ('NAO', 'Não Banheirista'),
)

TAMANHO_ROUPA = (
    ('P',      'P'),
    ('M',      'M'),
    ('G',      'G'),
    ('GG',     'GG'),
    ('EXTRAG', 'EXTRA GG'),
)

TAMANHO_CALCADO = (
    (34, '34'), (35, '35'), (36, '36'), (37, '37'),
    (38, '38'), (39, '39'), (40, '40'), (41, '41'),
    (42, '42'), (43, '43'), (44, '44'), (45, '45'),
)


# ─────────────────────────────────────────────
#  SETOR
# ─────────────────────────────────────────────

class Setor(models.Model):
    nome = models.CharField(
        max_length=40,
        verbose_name='Nome',
        null=False,
        unique=True,
        validators=[
            RegexValidator(
                r'^[a-zA-Z0-9áàâãéèêióôõúçñÁÀÂÃÉÈÊIÓÔÕÚÇÑ\s]+$',
                'Apenas letras são permitidas no nome.',
            )
        ],
    )

    # Encarregada responsável por este setor
    encarregada = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='setores',
        limit_choices_to={'role': 'encarregada'},
        verbose_name='Encarregada responsável',
    )

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


# ─────────────────────────────────────────────
#  FUNCIONÁRIO (colaborador — não é usuário)
# ─────────────────────────────────────────────

class Funcionario(models.Model):
    setores = models.ManyToManyField(
        Setor,
        blank=True,
        related_name='funcionarios',
    )

    # Encarregada responsável por este colaborador
    encarregada = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='funcionarios',
        limit_choices_to={'role': 'encarregada'},
        verbose_name='Encarregada responsável',
    )

    matricula_funcionario = models.PositiveIntegerField(primary_key=True)
    nome_funcionario = models.CharField(
        max_length=60,
        verbose_name='Nome Funcionário',
        blank=False,
        validators=[
            RegexValidator(
                r'^[a-zA-ZáàâãéèêióôõúçñÁÀÂÃÉÈÊIÓÔÕÚÇÑ\s]+$',
                'Apenas letras são permitidas no nome.',
            )
        ],
    )
    status = models.CharField(
        choices=STATUS,
        verbose_name='Status',
        max_length=3,
        null=False,
        default='NAO',
    )
    ferias = models.CharField(
        choices=FERIAS,
        verbose_name='Férias',
        max_length=3,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.nome_funcionario


# ─────────────────────────────────────────────
#  UNIFORME
# ─────────────────────────────────────────────

class Uniforme(models.Model):
    funcionario = models.OneToOneField(
        Funcionario,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='uniforme',
    )
    calca = models.CharField(
        choices=TAMANHO_ROUPA, max_length=6,
        verbose_name='Calça', null=False, blank=False,
    )
    blusa = models.CharField(
        choices=TAMANHO_ROUPA, max_length=6,
        verbose_name='Blusa', null=False, blank=False,
    )
    blusa_frio = models.CharField(
        choices=TAMANHO_ROUPA, max_length=6,
        verbose_name='Blusa de Frio', null=False, blank=False,
    )
    sapato = models.PositiveSmallIntegerField(
        choices=TAMANHO_CALCADO, verbose_name='Sapato',
        null=False, blank=False,
        validators=[MinValueValidator(34), MaxValueValidator(45)],
    )
    galocha = models.PositiveSmallIntegerField(
        choices=TAMANHO_CALCADO,
        null=False, blank=False,
        validators=[MinValueValidator(34), MaxValueValidator(45)],
    )