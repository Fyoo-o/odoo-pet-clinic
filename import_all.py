import csv, os
base = r'd:\UBIG\Proyek\odoo-pet-clinic\odoo pet clinic\csv_data'

def r(model, filename, fields):
    path = os.path.join(base, filename)
    with open(path, encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    result = env[model].load(fields, [[row[f] for f in fields] for row in rows])
    ids = result.get('ids') or []
    errs = [m for m in result.get('messages',[]) if m.get('type')=='error']
    print(f"[{'OK' if not errs else 'ERR'}] {model}: {len(ids)} | errs:{len(errs)}")
    [print(f"  {e.get('message','')}") for e in errs[:2]]

# 1. Pet Type
r('pet_clinic.pet_type', '01_pet_type.csv', ['name'])

# 2. Pet Breed - use ORM to resolve type_id by name
with open(os.path.join(base, '02_pet_breed.csv'), encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
created = 0
for row in rows:
    typ = env['pet_clinic.pet_type'].search([('name','=',row['type_id/name'])], limit=1)
    env['pet_clinic.pet_breed'].create({'name': row['name'], 'type_id': typ.id if typ else False})
    created += 1
env.cr.commit()
print(f"[OK] pet_clinic.pet_breed: {created} | errs:0")

# 3. Lokasi, Room, Doctor, Paramedis, Groomer
r('pet_clinic.lokasi',    '03_lokasi.csv',    ['name','address'])
r('pet_clinic.room',      '04_room.csv',      ['name','no_ruangan'])
r('pet_clinic.doctor',    '05_doctor.csv',    ['name','phone','specialization'])
r('pet_clinic.paramedis', '06_paramedis.csv', ['name','phone'])
r('pet_clinic.groomer',   '07_groomer.csv',   ['name','phone'])

# 8. Client
r('pet_clinic.client', '08_client.csv', ['name','phone','email','address'])
env.cr.commit()

# 9. Pet - resolve owner, type, breed by name
with open(os.path.join(base, '09_pet.csv'), encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
created = 0
for row in rows:
    owner  = env['pet_clinic.client'].search([('name','=',row['owner_id/name'])],  limit=1)
    typ    = env['pet_clinic.pet_type'].search([('name','=',row['type_id/name'])],  limit=1)
    breed  = env['pet_clinic.pet_breed'].search([('name','=',row['breed_id/name'])],limit=1)
    env['pet_clinic.pet'].create({
        'name': row['name'], 'gender': row['gender'],
        'date_of_birth': row['date_of_birth'] or False,
        'type_id': typ.id if typ else False,
        'breed_id': breed.id if breed else False,
        'owner_id': owner.id if owner else False,
    })
    created += 1
env.cr.commit()
print(f"[OK] pet_clinic.pet: {created} | errs:0")

# 10. Appointment
with open(os.path.join(base, '10_appointment.csv'), encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
created = 0
for row in rows:
    owner  = env['pet_clinic.client'].search([('name','=',row['owner_id/name'])], limit=1)
    pet    = env['pet_clinic.pet'].search([('name','=',row['pet_id/name'])],       limit=1)
    doc    = env['pet_clinic.doctor'].search([('name','=',row['doctor_id/name'])], limit=1)
    loc    = env['pet_clinic.lokasi'].search([('name','=',row['location_id/name'])],limit=1)
    room   = env['pet_clinic.room'].search([('name','=',row['room_id/name'])],     limit=1)
    env['pet_clinic.appointment'].create({
        'owner_id': owner.id if owner else False,
        'pet_id':   pet.id   if pet   else False,
        'doctor_id':doc.id   if doc   else False,
        'location_id': loc.id if loc  else False,
        'room_id':  room.id  if room  else False,
        'date':     row['date'],
        'state':    row['state'],
    })
    created += 1
env.cr.commit()
print(f"[OK] pet_clinic.appointment: {created} | errs:0")

# 11. Visitation
with open(os.path.join(base, '11_visitation.csv'), encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
created = 0
for row in rows:
    owner  = env['pet_clinic.client'].search([('name','=',row['owner_id/name'])],        limit=1)
    pet    = env['pet_clinic.pet'].search([('name','=',row['pet_id/name'])],               limit=1)
    doc    = env['pet_clinic.doctor'].search([('name','=',row['doctor_id/name'])],        limit=1)
    para   = env['pet_clinic.paramedis'].search([('name','=',row['paramedis_id/name'])],  limit=1)
    loc    = env['pet_clinic.lokasi'].search([('name','=',row['lokasi_pemeriksaan/name'])],limit=1)
    room   = env['pet_clinic.room'].search([('name','=',row['room_id/name'])],             limit=1)
    env['pet_clinic.visitation'].create({
        'owner_id': owner.id if owner else False,
        'pet_id':   pet.id   if pet   else False,
        'doctor_id':doc.id   if doc   else False,
        'paramedis_id': para.id if para else False,
        'lokasi_pemeriksaan': loc.id if loc else False,
        'room_id':  room.id  if room  else False,
        'date_start': row['date_start'],
        'penanganan': row['penanganan'],
        'weight':     float(row['weight']) if row['weight'] else 0,
        'temperature':float(row['temperature']) if row['temperature'] else 0,
        'keluhan_tujuan': row['keluhan_tujuan'],
        'diagnosis':  row['diagnosis'],
        'therapy':    row['therapy'],
        'state':      row['state'],
    })
    created += 1
env.cr.commit()
print(f"[OK] pet_clinic.visitation: {created} | errs:0")
print("\n=== ALL DONE ===")
