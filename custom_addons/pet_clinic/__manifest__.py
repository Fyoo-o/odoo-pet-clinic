# -*- coding: utf-8 -*-
{
    'name': 'Pet Clinic',
    'version': '18.0.1.0.0',
    'summary': 'Veterinary Clinic Management System',
    'description': """
        Pet Clinic - Sistem Manajemen Klinik Hewan
        ============================================
        Modul untuk mengelola klinik hewan meliputi:
        - Manajemen Pasien (Hewan Peliharaan)
        - Manajemen Client (Pemilik)
        - Kunjungan / Visitation
        - Layanan / Services
        - Appointment / Janji Temu
        - Dashboard & Laporan
        - Reminder & Notifikasi
        - Master Data
    """,
    'author': 'Pet Clinic Dev',
    'website': 'https://www.petclinic.com',
    'category': 'Services',
    'depends': [
        'base',
        'mail',
        'product',
        'point_of_sale',
        'sale',
        'account',
        'calendar',
    ],
    'data': [
        # Security
        'security/pet_clinic_security.xml',
        'security/ir.model.access.csv',
        # Data
        'data/ir_sequence_data.xml',
        # Reports (must load before views that reference report actions)
        'report/pet_clinic_report.xml',
        # Views
        'views/pet_clinic_client_views.xml',
        'views/pet_clinic_pet_views.xml',
        'views/pet_clinic_visitation_views.xml',
        'views/pet_clinic_service_views.xml',
        'views/pet_clinic_appointment_views.xml',
        'views/pet_clinic_master_data_views.xml',
        'views/pet_clinic_dashboard_views.xml',
        'views/pet_clinic_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pet_clinic/static/src/js/dashboard.js',
            'pet_clinic/static/src/xml/dashboard_templates.xml',
            'pet_clinic/static/src/css/dashboard.css',
            'pet_clinic/static/src/css/navbar.css',
        ],
    },
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
