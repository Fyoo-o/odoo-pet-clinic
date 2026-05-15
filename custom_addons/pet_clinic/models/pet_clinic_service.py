# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PetClinicService(models.Model):
    _name = 'pet_clinic.service'
    _description = 'Service / Layanan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(
        string='Service No.',
        readonly=True,
        copy=False,
        default='New',
        tracking=True,
    )
    visitation_id = fields.Many2one(
        'pet_clinic.visitation', string='Visitation', ondelete='cascade',
    )
    pet_id = fields.Many2one(
        'pet_clinic.pet', string='Pet', tracking=True,
    )
    nama_pemilik = fields.Many2one(
        'pet_clinic.client', string='Owner',
    )
    visitation_lokasi_id = fields.Many2one(
        'pet_clinic.lokasi', related='visitation_id.lokasi_pemeriksaan',
        string='Lokasi Pemeriksaan', store=True,
    )
    service_type = fields.Many2one(
        'product.product', string='Service',
        domain="[('type', '=', 'service'), ('lokasi_ids', '=?', visitation_lokasi_id)]",
    )
    dokter_penerima = fields.Many2one(
        'pet_clinic.doctor', string='Dokter Penerima',
        domain="[('lokasi_ids', '=?', visitation_lokasi_id)]",
    )
    dokter_dp_ip = fields.Many2one(
        'pet_clinic.doctor', string='Dokter DP/IP',
        domain="[('lokasi_ids', '=?', visitation_lokasi_id)]",
    )
    groomer_id = fields.Many2one(
        'pet_clinic.groomer', string='Groomer',
        domain="[('lokasi_ids', '=?', visitation_lokasi_id)]",
    )
    paramedis_id = fields.Many2one(
        'pet_clinic.paramedis', string='Paramedis',
        domain="[('lokasi_ids', '=?', visitation_lokasi_id)]",
    )
    penanggung_jawab_name = fields.Char(
        string='Penanggung Jawab',
        compute='_compute_penanggung_jawab_name',
        store=True,
    )
    date_handling = fields.Date(
        string='Date Handling', default=fields.Date.today,
    )
    amount = fields.Float(string='Amount', default=1)
    unit_price = fields.Float(
        string='Unit Price',
        related='service_type.list_price',
        store=True,
    )
    total_price = fields.Float(
        string='Total Price',
        compute='_compute_total_price',
        store=True,
    )
    category = fields.Many2one(
        'product.category', string='Category',
        related='service_type.categ_id',
        store=True,
    )
    referensi_pos_order = fields.Many2one(
        'pos.order', string='POS Order Reference',
    )
    service_detail_ids = fields.One2many(
        'pet_clinic.service_detail', 'service_id',
        string='Service Details',
    )

    @api.depends('amount', 'unit_price')
    def _compute_total_price(self):
        for rec in self:
            rec.total_price = rec.amount * rec.unit_price

    @api.depends('dokter_penerima', 'groomer_id', 'paramedis_id')
    def _compute_penanggung_jawab_name(self):
        for rec in self:
            names = []
            if rec.dokter_penerima:
                names.append(rec.dokter_penerima.name)
            if rec.groomer_id:
                names.append(rec.groomer_id.name)
            if rec.paramedis_id:
                names.append(rec.paramedis_id.name)
            rec.penanggung_jawab_name = ', '.join(names) if names else ''

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'pet_clinic.service'
                ) or 'New'
        return super().create(vals_list)

    @api.onchange('visitation_id')
    def _onchange_visitation_id(self):
        if self.visitation_id:
            self.pet_id = self.visitation_id.pet_id
            self.nama_pemilik = self.visitation_id.owner_id

    def action_create_pos_order(self):
        """Create POS Order from service."""
        self.ensure_one()
        pos_session = self.env['pos.session'].search(
            [('state', '=', 'opened')], limit=1,
        )
        if not pos_session:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Warning',
                    'message': 'No open POS session found. Please open a POS session first.',
                    'type': 'warning',
                },
            }

        partner = False
        if self.nama_pemilik:
            partner = self.env['res.partner'].search(
                [('name', '=', self.nama_pemilik.name)], limit=1,
            )

        pos_order = self.env['pos.order'].create({
            'session_id': pos_session.id,
            'partner_id': partner.id if partner else False,
            'lines': [(0, 0, {
                'product_id': self.service_type.id,
                'qty': self.amount,
                'price_unit': self.unit_price,
                'price_subtotal': self.total_price,
                'price_subtotal_incl': self.total_price,
            })],
        })
        self.referensi_pos_order = pos_order.id

        return {
            'type': 'ir.actions.act_window',
            'name': 'POS Order',
            'res_model': 'pos.order',
            'view_mode': 'form',
            'res_id': pos_order.id,
        }


class PetClinicServiceDetail(models.Model):
    _name = 'pet_clinic.service_detail'
    _description = 'Service Detail Checklist'

    service_id = fields.Many2one(
        'pet_clinic.service', string='Service', ondelete='cascade',
    )
    name = fields.Char(string='Detail')
    is_done = fields.Boolean(string='Done')
