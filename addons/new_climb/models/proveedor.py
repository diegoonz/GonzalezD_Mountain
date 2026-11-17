from odoo import models
from odoo import fields

#clase Proveedor para almacenar información sobre los proveedores de material de montaña
class Proveedor(models.Model):
    _name = 'new_climb.proveedor'
    _description = 'Proveedor de material de New Climb'

    #datos del proveedor para identificarlo
    name = fields.Char(string='Nombre del proveedor', required=True)
    direccion = fields.Char(string='Dirección')
    telefono = fields.Char(string='Teléfono')
    email = fields.Char(string='Correo electrónico')
    website = fields.Char(string='Sitio web')


    #datos del proveedor para gestionarlo
    actividad = fields.Selection([
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ], string='Estado', default='activo')
    tipo = fields.Selection([
        ('ropa', 'Ropa'),
        ('material_tecnico', 'Material Técnico'),
    ], string='Tipo de proveedor')

    #relacion con el material que suministra
    material_ids = fields.One2many('new_climb.material', 'proveedor_id', string='Material suministrado')

