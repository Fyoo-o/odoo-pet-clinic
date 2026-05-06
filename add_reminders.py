"""Tambahkan data untuk semua model Reminder yang kosong"""

# 1. Notif Reminder (H-x sebelum appointment)
notif_reminders = [
    {'name': 'Reminder H-7 Appointment',   'days_before': 7,  'template': 'Halo {owner_name}, mengingatkan bahwa {pet_name} memiliki jadwal pemeriksaan 7 hari lagi pada {date}. Terima kasih.'},
    {'name': 'Reminder H-3 Appointment',   'days_before': 3,  'template': 'Halo {owner_name}, 3 hari lagi {pet_name} memiliki jadwal kunjungan ke klinik kami pada {date}. Sampai jumpa!'},
    {'name': 'Reminder H-1 Appointment',   'days_before': 1,  'template': 'Halo {owner_name}, besok {pet_name} jadwal kunjungan ke klinik. Pastikan {pet_name} sudah siap ya!'},
    {'name': 'Reminder Hari H Appointment','days_before': 0,  'template': 'Halo {owner_name}, hari ini {pet_name} memiliki jadwal pemeriksaan. Kami tunggu kedatangannya!'},
    {'name': 'Reminder H-14 Vaksin',       'days_before': 14, 'template': 'Halo {owner_name}, 2 minggu lagi jadwal vaksinasi rutin {pet_name}. Segera buat appointment!'},
]
for r in notif_reminders:
    env['pet_clinic.notif_reminder'].create(r)
env.cr.commit()
print(f"[OK] notif_reminder: {len(notif_reminders)} records")

# 2. Notif Reminder Checkup (H+x setelah visitation selesai)
checkup_reminders = [
    {'name': 'Checkup Follow-Up 7 Hari',  'days_after': 7},
    {'name': 'Checkup Follow-Up 14 Hari', 'days_after': 14},
    {'name': 'Checkup Follow-Up 30 Hari', 'days_after': 30},
    {'name': 'Checkup Pasca Operasi 3 Hari','days_after': 3},
    {'name': 'Checkup Vaksin Booster 21 Hari','days_after': 21},
]
for r in checkup_reminders:
    env['pet_clinic.notif_reminder_checkup'].create(r)
env.cr.commit()
print(f"[OK] notif_reminder_checkup: {len(checkup_reminders)} records")

# 3. Notif After Service
after_service = [
    {'name': 'Follow-Up Pasca Konsultasi', 'days_after': 3},
    {'name': 'Follow-Up Pasca Grooming',   'days_after': 7},
    {'name': 'Follow-Up Pasca Operasi',    'days_after': 1},
    {'name': 'Survei Kepuasan Layanan',    'days_after': 1},
]
for r in after_service:
    env['pet_clinic.notif_after_service'].create(r)
env.cr.commit()
print(f"[OK] notif_after_service: {len(after_service)} records")

# 4. Notif (general notification)
notifs = [
    {'name': 'Notif Kunjungan Baru',     'type': 'info',    'content': 'Ada kunjungan baru yang masuk. Segera proses di modul Kunjungan.'},
    {'name': 'Notif Stok Obat Menipis',  'type': 'warning', 'content': 'Stok obat beberapa item hampir habis. Segera lakukan pemesanan ulang.'},
    {'name': 'Notif Jadwal Penuh',       'type': 'warning', 'content': 'Jadwal dokter sudah penuh untuk hari ini. Informasikan kepada pasien baru.'},
    {'name': 'Notif Darurat Pasien',     'type': 'urgent',  'content': 'Ada pasien dalam kondisi darurat. Segera hubungi dokter jaga!'},
    {'name': 'Notif Update Sistem',      'type': 'info',    'content': 'Sistem akan diperbarui pada pukul 23:00. Simpan semua pekerjaan Anda.'},
]
for n in notifs:
    env['pet_clinic.notif'].create(n)
env.cr.commit()
print(f"[OK] notif: {len(notifs)} records")

# 5. Client Activate
client_activates = [
    {'name': 'Template Aktivasi Akun',      'template': 'Selamat datang {client_name}! Akun Anda telah berhasil diaktifkan. Terima kasih telah bergabung dengan Pet Clinic kami.'},
    {'name': 'Template Selamat Bergabung',  'template': 'Halo {client_name}! Selamat datang di keluarga besar Pet Clinic. Kami siap merawat {pet_name} dengan sepenuh hati.'},
]
for c in client_activates:
    env['pet_clinic.client_activate'].create(c)
env.cr.commit()
print(f"[OK] client_activate: {len(client_activates)} records")

# 6. Client Reset Password
reset_passwords = [
    {'name': 'Template Reset Password',  'template': 'Halo {client_name}, kami menerima permintaan reset password untuk akun Anda. Klik link berikut untuk membuat password baru.'},
    {'name': 'Template Konfirmasi Reset','template': 'Password akun {client_name} telah berhasil direset. Jika Anda tidak melakukan ini, segera hubungi kami.'},
]
for r in reset_passwords:
    env['pet_clinic.client_reset_password'].create(r)
env.cr.commit()
print(f"[OK] client_reset_password: {len(reset_passwords)} records")

print("\n=== SEMUA REMINDER DATA BERHASIL DIISI ===")
