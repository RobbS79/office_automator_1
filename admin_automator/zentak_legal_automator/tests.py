from django.test import TestCase
from django.urls import reverse
from .models import Employee

class EmployeeFormViewTest(TestCase):

    def setUp(self):
        # Initial setup: create an employee record to start with
        Employee.objects.create(
            zamestnanec_titul_pred_menom="Mr.",
            zamestnanec_meno="John",
            zamestnanec_priezvisko="Doe",
            zamestnanec_titul_za_menom="PhD",
            zamestnanec_datum_narodenia="1990-01-01",
            zamestnanec_miesto_narodenia="City",
            zamestnanec_statna_prislusnost="Country",
            zamestnanec_rodne_priezvisko="Doe",
            zamestnanec_rodne_cislo="123456789",
            zamestnanec_adresa_ulica="Street 123",
            zamestnanec_adresa_mesto="Cityville",
            zamestnanec_adresa_psc="12345",
            zamestnanec_adresa_stat="Country",
            zamestnanec_tel_cislo="1234567890",
            zamestnanec_email="john.doe@example.com",
            zamestnanec_cudzinec_doklad_pobyt="Yes",
            zamestnanec_cudzinec_pracovne_povolenie="Yes",
            zamestnanec_korespondencna_adresa="Korespondencna 123",
            andresa_na_dorucenie_pda1="PDA 123",
            zamestnanec_pracovna_napln_pred_vyslanim="Work details",
            zamestnanec_vyslany_od="2025-01-01",
            zamestnanec_vyslany_do="2025-12-31",
            zamestnanec_druh_cinnosti_pri_vyslani="Activity",
            druh_cinnosti_kod_nace="1234",
            podpis_zamestnanec_miesto="City",
            podpis_zamestnanec_datum="2025-01-01",
            zamestnanec_pohlavie_muz=False,
            zamestnanec_pohlavie_zena=True,
            zamestnanec_vyslany_prideleny_inej_firme_ano=False,
            zamestnanec_vyslany_prideleny_inej_firme_nie=True,
            zamestnanec_subezny_uvazok_inej_firme_ano=False,
            zamestnanec_subezny_uvazok_inej_firme_nie=True,
            zamestnanec_odmena_od_kmenovej_firmy_ano=False,
            zamestnanec_odmena_od_kmenovej_firmy_nie=True,
            zamestnanec_zadanie_prace_kmenovou_firmou_ano=False,
            zamestnanec_zadanie_prace_kmenovou_firmou_nie=True,
            zamestnanec_nahradza_zamestnanca_ano=False,
            zamestnanec_nahradza_zamestnanca_nie=True,
            zamestnanec_vystaveny_E101_PDA1_v_inej_krajine_ano=False,
            zamestnanec_vystaveny_E101_PDA1_v_inej_krajine_nie=True,
        )

    def test_employee_form_submission(self):
        # Get the initial number of employees in the table
        initial_count = Employee.objects.count()

        # Data to be submitted via the form
        data = {
            'zamestnanec_titul_pred_menom': 'Mr.',
            'zamestnanec_meno': 'Alice',
            'zamestnanec_priezvisko': 'Smith',
            'zamestnanec_titul_za_menom': 'MD',
            'zamestnanec_datum_narodenia': '1985-05-15',
            'zamestnanec_miesto_narodenia': 'Town',
            'zamestnanec_statna_prislusnost': 'Country',
            'zamestnanec_rodne_priezvisko': 'Smith',
            'zamestnanec_rodne_cislo': '987654321',
            'zamestnanec_adresa_ulica': 'Main St 456',
            'zamestnanec_adresa_mesto': 'Cityplace',
            'zamestnanec_adresa_psc': '67890',
            'zamestnanec_adresa_stat': 'Country',
            'zamestnanec_tel_cislo': '0987654321',
            'zamestnanec_email': 'alice.smith@example.com',
            'zamestnanec_cudzinec_doklad_pobyt': 'No',
            'zamestnanec_cudzinec_pracovne_povolenie': 'No',
            'zamestnanec_korespondencna_adresa': 'Korespondencia 456',
            'andresa_na_dorucenie_pda1': 'PDA456',
            'zamestnanec_pracovna_napln_pred_vyslanim': 'New job details',
            'zamestnanec_vyslany_od': '2025-02-01',
            'zamestnanec_vyslany_do': '2025-11-30',
            'zamestnanec_druh_cinnosti_pri_vyslani': 'New activity',
            'druh_cinnosti_kod_nace': '5678',
            'podpis_zamestnanec_miesto': 'New City',
            'podpis_zamestnanec_datum': '2025-02-01',
            'zamestnanec_pohlavie_muz': False,
            'zamestnanec_pohlavie_zena': True,
            'zamestnanec_vyslany_prideleny_inej_firme_ano': False,
            'zamestnanec_vyslany_prideleny_inej_firme_nie': True,
            'zamestnanec_subezny_uvazok_inej_firme_ano': False,
            'zamestnanec_subezny_uvazok_inej_firme_nie': True,
            'zamestnanec_odmena_od_kmenovej_firmy_ano': False,
            'zamestnanec_odmena_od_kmenovej_firmy_nie': True,
            'zamestnanec_zadanie_prace_kmenovou_firmou_ano': False,
            'zamestnanec_zadanie_prace_kmenovou_firmou_nie': True,
            'zamestnanec_nahradza_zamestnanca_ano': False,
            'zamestnanec_nahradza_zamestnanca_nie': True,
            'zamestnanec_vystaveny_E101_PDA1_v_inej_krajine_ano': False,
            'zamestnanec_vystaveny_E101_PDA1_v_inej_krajine_nie': True,
        }

        # Submit the form via POST request
        response = self.client.post(reverse('onboarding_form'), data)

        # Get the final number of employees in the table
        final_count = Employee.objects.count()

        # Assert that the number of employees increased by exactly 1
        self.assertEqual(final_count, initial_count + 1)
