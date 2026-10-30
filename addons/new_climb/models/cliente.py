from odoo import models, fields

#clase cliente para almacenar información sobre los clientes de material de montaña
class Cliente(models.Model):
    _name = 'new_climb.cliente'
    _description = 'Cliente de material de New Climb'

    #datos del cliente para identificarlo
    name = fields.Char(string='Nombre del cliente', required=True)
    direccion = fields.Char(string='Dirección')
    telefono = fields.Char(string='Teléfono')
    email = fields.Char(string='Correo electrónico')

    #datos del cliente para gestionarlo
    fecha_registro = fields.Date(string='Fecha de registro', default=fields.Date.today)
    socio_premium = fields.Boolean(string='Socio premium', default=False)
    observaciones = fields.Text(string='Observaciones')