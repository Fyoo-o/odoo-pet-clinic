#!/usr/bin/env python3
"""Script to delete all pet_clinic data in correct order (respecting FK constraints)"""

# Delete in reverse dependency order
models_to_delete = [
    # Detail/line records first
    'pet_clinic.medical_history_line',
    'pet_clinic.visitation_barang',
    'pet_clinic.visitation_item',
    # Transactional records
    'pet_clinic.service',
    'pet_clinic.appointment',
    'pet_clinic.visitation',
    # Patient records
    'pet_clinic.pet',
    'pet_clinic.client',
    # Master data with dependencies
    'pet_clinic.pet_breed',
    'pet_clinic.pet_type',
    'pet_clinic.doctor',
    'pet_clinic.paramedis',
    'pet_clinic.groomer',
    'pet_clinic.room',
    'pet_clinic.lokasi',
    'pet_clinic.kecamatan',
    'pet_clinic.kab_kota',
    'pet_clinic.provinsi',
    'pet_clinic.diagnosa',
    'pet_clinic.dosis',
    'pet_clinic.notif',
    'pet_clinic.notif_reminder',
    'pet_clinic.notif_reminder_checkup',
    'pet_clinic.notif_after_service',
    'pet_clinic.client_activate',
    'pet_clinic.client_reset_password',
    'pet_clinic.promo',
    'pet_clinic.banner',
    'pet_clinic.blog',
    'pet_clinic.event',
]

total_deleted = 0
for model_name in models_to_delete:
    try:
        records = env[model_name].search([])
        count = len(records)
        if count:
            records.unlink()
            print(f"[OK] Deleted {count} records from {model_name}")
            total_deleted += count
        else:
            print(f"[--] No records in {model_name}")
    except Exception as e:
        print(f"[ERR] {model_name}: {e}")

env.cr.commit()
print(f"\n=== DONE: Total {total_deleted} records deleted ===")
