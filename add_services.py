"""
Tambahkan data service ke dalam setiap visitation yang sudah ada.
Service di Pet Clinic adalah baris layanan di dalam tab Services pada form Kunjungan.
"""

# Cari produk tipe service yang ada di database
services_available = env['product.product'].search([('type', '=', 'service')], limit=10)
print("Produk service tersedia:", [s.name for s in services_available])

# Jika tidak ada produk service, buat beberapa dulu
if not services_available:
    categ = env['product.category'].search([('name', '=', 'All')], limit=1)
    service_products = [
        {'name': 'Konsultasi Umum',    'list_price': 75000},
        {'name': 'Vaksinasi Rabies',   'list_price': 150000},
        {'name': 'Operasi Sterilisasi','list_price': 500000},
        {'name': 'Grooming Basic',     'list_price': 100000},
        {'name': 'Rawat Inap (per hari)', 'list_price': 200000},
        {'name': 'Rontgen',            'list_price': 250000},
        {'name': 'Cek Laboratorium',   'list_price': 180000},
    ]
    created_products = []
    for sp in service_products:
        p = env['product.product'].create({
            'name': sp['name'],
            'type': 'service',
            'list_price': sp['list_price'],
            'categ_id': categ.id if categ else False,
        })
        created_products.append(p)
    env.cr.commit()
    print(f"Dibuat {len(created_products)} produk service baru")
    services_available = env['product.product'].search([('type', '=', 'service')], limit=10)

# Mapping layanan per visitation berdasarkan diagnosis
visitation_service_map = {
    # visitation owner -> list of (service_product_name, amount)
    'Agus Wijaya':   [('Konsultasi Umum', 1)],
    'Budi Hartono':  [('Konsultasi Umum', 1), ('Grooming Basic', 1)],
    'Citra Lestari': [('Konsultasi Umum', 1), ('Rawat Inap (per hari)', 3)],
    'Dewi Rahayu':   [('Konsultasi Umum', 1), ('Cek Laboratorium', 1)],
    'Irwan Kusuma':  [('Konsultasi Umum', 1)],
    'Jasmine Putri': [('Konsultasi Umum', 1), ('Vaksinasi Rabies', 1)],
}

visitations = env['pet_clinic.visitation'].search([])
total_services = 0
for vis in visitations:
    owner_name = vis.owner_id.name if vis.owner_id else ''
    svc_list = visitation_service_map.get(owner_name, [('Konsultasi Umum', 1)])
    for svc_name, amount in svc_list:
        product = env['product.product'].search([('name', '=', svc_name), ('type', '=', 'service')], limit=1)
        if not product:
            product = services_available[0] if services_available else False
        if product:
            env['pet_clinic.service'].create({
                'visitation_id':  vis.id,
                'pet_id':         vis.pet_id.id if vis.pet_id else False,
                'nama_pemilik':   vis.owner_id.id if vis.owner_id else False,
                'service_type':   product.id,
                'dokter_penerima':vis.doctor_id.id if vis.doctor_id else False,
                'amount':         amount,
            })
            total_services += 1

env.cr.commit()
print(f"\n=== SELESAI: {total_services} service records dibuat ===")
