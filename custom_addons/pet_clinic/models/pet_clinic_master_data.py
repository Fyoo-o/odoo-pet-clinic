# -*- coding: utf-8 -*-
from odoo import models, fields


class PetClinicPetType(models.Model):
    _name = 'pet_clinic.pet_type'
    _description = 'Pet Type'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    breed_ids = fields.One2many(
        'pet_clinic.pet_breed', 'type_id', string='Breeds',
    )


class PetClinicPetBreed(models.Model):
    _name = 'pet_clinic.pet_breed'
    _description = 'Pet Breed'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    type_id = fields.Many2one(
        'pet_clinic.pet_type', string='Pet Type',
    )


class PetClinicDoctor(models.Model):
    _name = 'pet_clinic.doctor'
    _description = 'Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Name', required=True, tracking=True)
    phone = fields.Char(string='Phone')
    specialization = fields.Char(string='Specialization')
    active = fields.Boolean(default=True)
    lokasi_ids = fields.Many2many(
        'pet_clinic.lokasi', string='Cabang / Lokasi',
    )


class PetClinicParamedis(models.Model):
    _name = 'pet_clinic.paramedis'
    _description = 'Paramedis'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone')
    lokasi_ids = fields.Many2many(
        'pet_clinic.lokasi', string='Cabang / Lokasi',
    )


class PetClinicGroomer(models.Model):
    _name = 'pet_clinic.groomer'
    _description = 'Groomer'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone')
    lokasi_ids = fields.Many2many(
        'pet_clinic.lokasi', string='Cabang / Lokasi',
    )


class PetClinicRoom(models.Model):
    _name = 'pet_clinic.room'
    _description = 'Room'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    no_ruangan = fields.Char(string='No. Ruangan')
    lokasi_ids = fields.Many2many(
        'pet_clinic.lokasi', string='Cabang / Lokasi',
    )


class PetClinicLokasi(models.Model):
    _name = 'pet_clinic.lokasi'
    _description = 'Lokasi'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    address = fields.Char(string='Address')


class PetClinicProvinsi(models.Model):
    _name = 'pet_clinic.provinsi'
    _description = 'Provinsi'
    _order = 'name'

    name = fields.Char(string='Name', required=True)


class PetClinicKabKota(models.Model):
    _name = 'pet_clinic.kab_kota'
    _description = 'Kabupaten/Kota'
    _order = 'name'

    name = fields.Char(string='Name', required=True)


class PetClinicKecamatan(models.Model):
    _name = 'pet_clinic.kecamatan'
    _description = 'Kecamatan'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    kab_kota_id = fields.Many2one(
        'pet_clinic.kab_kota', string='Kab/Kota',
    )


class PetClinicBanner(models.Model):
    _name = 'pet_clinic.banner'
    _description = 'Banner'

    name = fields.Char(string='Name', required=True)
    image = fields.Binary(string='Image', attachment=True)
    url = fields.Char(string='URL')


class PetClinicBlog(models.Model):
    _name = 'pet_clinic.blog'
    _description = 'Blog'

    name = fields.Char(string='Name', required=True)
    content = fields.Html(string='Content')


class PetClinicEvent(models.Model):
    _name = 'pet_clinic.event'
    _description = 'Event'
    _order = 'date desc'

    name = fields.Char(string='Name', required=True)
    date = fields.Datetime(string='Date')
    description = fields.Text(string='Description')


class PetClinicNotif(models.Model):
    _name = 'pet_clinic.notif'
    _description = 'Notification'

    name = fields.Char(string='Name', required=True)
    content = fields.Text(string='Content')
    type = fields.Selection(
        [
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('urgent', 'Urgent'),
        ],
        string='Type', default='info',
    )


class PetClinicPromo(models.Model):
    _name = 'pet_clinic.promo'
    _description = 'Promo'

    name = fields.Char(string='Name', required=True)
    discount = fields.Float(string='Discount (%)')
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')


class PetClinicNotifReminder(models.Model):
    _name = 'pet_clinic.notif_reminder'
    _description = 'Notif Reminder'

    name = fields.Char(string='Name', required=True)
    template = fields.Text(string='Template')
    days_before = fields.Integer(string='Days Before')


class PetClinicClientActivate(models.Model):
    _name = 'pet_clinic.client_activate'
    _description = 'Client Activate'

    name = fields.Char(string='Name', required=True)
    template = fields.Text(string='Template')


class PetClinicClientResetPassword(models.Model):
    _name = 'pet_clinic.client_reset_password'
    _description = 'Client Reset Password'

    name = fields.Char(string='Name', required=True)
    template = fields.Text(string='Template')


class PetClinicNotifReminderCheckup(models.Model):
    _name = 'pet_clinic.notif_reminder_checkup'
    _description = 'Notif Reminder Checkup'

    name = fields.Char(string='Name', required=True)
    days_after = fields.Integer(string='Days After')


class PetClinicNotifAfterService(models.Model):
    _name = 'pet_clinic.notif_after_service'
    _description = 'Notif After Service'

    name = fields.Char(string='Name', required=True)
    days_after = fields.Integer(string='Days After')


class PetClinicDiagnosa(models.Model):
    _name = 'pet_clinic.diagnosa'
    _description = 'Diagnosa'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


class PetClinicDosis(models.Model):
    _name = 'pet_clinic.dosis'
    _description = 'Dosis'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    quantity = fields.Float(string='Quantity')
