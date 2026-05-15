import psycopg2
import json

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    dbname='odoo-pet-clinic',
    user='odoo',
    password='admin'
)
cur = conn.cursor()

print("=" * 60)
print("LOKASI / CABANG")
print("=" * 60)
cur.execute("SELECT id, name, address FROM pet_clinic_lokasi ORDER BY id;")
for row in cur.fetchall():
    print(f"  ID:{row[0]} | {row[1]} | {row[2]}")

print("\n" + "=" * 60)
print("DOKTER")
print("=" * 60)
cur.execute("SELECT id, name FROM pet_clinic_doctor ORDER BY id;")
for row in cur.fetchall():
    print(f"  ID:{row[0]} | {row[1]}")

print("\n" + "=" * 60)
print("CLIENT / MEMBER (10 pertama)")
print("=" * 60)
cur.execute("SELECT id, name FROM pet_clinic_client ORDER BY id LIMIT 10;")
for row in cur.fetchall():
    print(f"  ID:{row[0]} | {row[1]}")

cur.execute("SELECT COUNT(*) FROM pet_clinic_client;")
total = cur.fetchone()[0]
print(f"  ... (Total: {total} client)")

print("\n" + "=" * 60)
print("HEWAN / PET (10 pertama)")
print("=" * 60)
cur.execute("SELECT id, name FROM pet_clinic_pet ORDER BY id LIMIT 10;")
for row in cur.fetchall():
    print(f"  ID:{row[0]} | {row[1]}")

cur.execute("SELECT COUNT(*) FROM pet_clinic_pet;")
total = cur.fetchone()[0]
print(f"  ... (Total: {total} hewan)")

print("\n" + "=" * 60)
print("KUNJUNGAN / VISITATION (5 pertama & terakhir)")
print("=" * 60)
cur.execute("SELECT id, name FROM pet_clinic_visitation ORDER BY id LIMIT 5;")
for row in cur.fetchall():
    print(f"  ID:{row[0]} | {row[1]}")

cur.execute("SELECT COUNT(*) FROM pet_clinic_visitation;")
total = cur.fetchone()[0]
print(f"  ... (Total: {total} kunjungan)")

print("\n" + "=" * 60)
print("JANJI TEMU / APPOINTMENT (5 pertama)")
print("=" * 60)
cur.execute("SELECT id, name FROM pet_clinic_appointment ORDER BY id LIMIT 5;")
for row in cur.fetchall():
    print(f"  ID:{row[0]} | {row[1]}")

cur.execute("SELECT COUNT(*) FROM pet_clinic_appointment;")
total = cur.fetchone()[0]
print(f"  ... (Total: {total} janji)")

cur.close()
conn.close()
print("\nDone.")
