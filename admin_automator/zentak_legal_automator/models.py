from django.db import models


class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('partner', 'Partner'),
        ('viewer', 'Viewer')
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """
        Set a hashed password (e.g., using Django's make_password utility).
        """
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Check if the given raw password matches the hashed password.
        """
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)



class Employee(models.Model):
    id_employee = models.IntegerField(primary_key=True)
    zamestnanec_titul_pred_menom = models.CharField(max_length=100,null=True,blank=True)
    zamestnanec_meno = models.CharField(max_length=100,null=True,blank=True)
    zamestnanec_priezvisko = models.CharField(max_length=100,null=True,blank=True)
    zamestnanec_titul_za_menom = models.CharField(max_length=100,null=True,blank=True)
    zamestnanec_datum_narodenia = models.DateField(null=True,blank=True)
    zamestnanec_miesto_narodenia = models.CharField(max_length=100,null=True,blank=True)
    zamestnanec_statna_prislusnost = models.CharField(max_length=100,null=True,blank=True)
    zamestnanec_rodne_priezvisko = models.CharField(max_length=100,null=True,blank=True)
    zamestnanec_rodne_cislo = models.CharField(max_length=20,null=True,blank=True)
    zamestnanec_adresa_ulica = models.CharField(max_length=200,null=True,blank=True)
    zamestnanec_adresa_mesto = models.CharField(max_length=100,null=True,blank=True)
    zamestnanec_adresa_psc = models.CharField(max_length=10,null=True,blank=True)
    zamestnanec_adresa_stat = models.CharField(max_length=100,null=True,blank=True)
    zamestnanec_tel_cislo = models.CharField(max_length=20,null=True,blank=True)
    zamestnanec_email = models.EmailField(null=True,blank=True)
    zamestnanec_cudzinec_doklad_pobyt = models.CharField(max_length=100, null=True, blank=True)
    zamestnanec_cudzinec_pracovne_povolenie = models.CharField(max_length=100, null=True, blank=True)
    zamestnanec_korespondencna_adresa = models.CharField(max_length=200, null=True, blank=True)
    podpis_zamestnanec_miesto = models.CharField(max_length=100, null=True, blank=True)
    podpis_zamestnanec_datum = models.DateField(null=True, blank=True)
    zamestnanec_pohlavie_muz = models.BooleanField(default=False)
    zamestnanec_pohlavie_zena = models.BooleanField(default=False)

    class Meta:
        db_table = 'employees'

    def __str__(self):
        return f'{self.zamestnanec_meno} {self.zamestnanec_priezvisko}'


class EmployeeAgreement(models.Model):
    id_employee_agreement = models.AutoField(primary_key=True)
    id_employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    zamestnanec_pracovna_napln_pred_vyslanim = models.TextField(null=True, blank=True)
    employee_agreement_type = models.Choices("pda1_requests","loan","investment","PPE")
    zamestnanec_vyslany_od = models.DateField(null=True, blank=True)#only for pda1_requests
    zamestnanec_vyslany_do = models.DateField(null=True, blank=True)#only for pda1_requests
    zamestnanec_druh_cinnosti_pri_vyslani = models.CharField(max_length=100, null=True, blank=True)#only for pda1_requests
    druh_cinnosti_kod_nace = models.CharField(max_length=10, null=True, blank=True)#only for pda1_requests
    andresa_na_dorucenie_pda1 = models.CharField(max_length=200, null=True, blank=True)#only for pda1_requests
    zamestnanec_vyslany_prideleny_inej_firme_ano = models.BooleanField(default=False)#only for pda1_requests
    zamestnanec_vyslany_prideleny_inej_firme_nie = models.BooleanField(default=False)#only for pda1_requests
    zamestnanec_subezny_uvazok_inej_firme_ano = models.BooleanField(default=False)#only for pda1_requests
    zamestnanec_subezny_uvazok_inej_firme_nie = models.BooleanField(default=False)#only for pda1_requests
    zamestnanec_odmena_od_kmenovej_firmy_ano = models.BooleanField(default=False)#only for pda1_requests
    zamestnanec_odmena_od_kmenovej_firmy_nie = models.BooleanField(default=False)#only for pda1_requests
    zamestnanec_zadanie_prace_kmenovou_firmou_ano = models.BooleanField(default=False)#only for pda1_requests
    zamestnanec_zadanie_prace_kmenovou_firmou_nie = models.BooleanField(default=False)#only for pda1_requests
    zamestnanec_nahradza_zamestnanca_ano = models.BooleanField(default=False)#only for pda1_requests
    zamestnanec_nahradza_zamestnanca_nie = models.BooleanField(default=False)#only for pda1_requests
    zamestnanec_vystaveny_E101_PDA1_v_inej_krajine_ano = models.BooleanField(default=False)#only for pda1_requests
    zamestnanec_vystaveny_E101_PDA1_v_inej_krajine_nie = models.BooleanField(default=False)#only for pda1_requests

    # Metadata
    class Meta:
        db_table = 'employees_agreements'  # specify the actual table name

    def __str__(self):
        return f'Employee ID: {self.id_employee} and his: {self.employee_agreement_type}'