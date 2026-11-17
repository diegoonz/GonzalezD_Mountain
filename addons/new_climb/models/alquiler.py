from odoo import models
from odoo import fields
from datetime import timedelta
from odoo import api
from odoo.exceptions import ValidationError 

class Alquiler(models.Model):
    _name = 'new_climb.alquiler'
    _description = 'Alquiler de material de New Climb'

    #datos del alquiler para identificarlo
    name = fields.Char(string='Nombre del alquiler', required=True)
    fecha_alquiler = fields.Date(string='Fecha de alquiler', default=fields.Date.today)

    #datos calculo automático
    precio_total = fields.Float(string='Precio total')

    #relacion con el material alquilado
    material_id = fields.Many2many('new_climb.material', string='Material alquilado')
    cliente_id = fields.Many2one('new_climb.cliente', string='Cliente que alquila', ondelete='set null', index=True)

    #relacion con el proveedor del material alquilado
    proveedor_id = fields.Many2one('new_climb.proveedor', string='Proveedor del material alquilado', ondelete='set null', index=True)
    fecha_devolucion = fields.Datetime(string='Fecha de devolución', default=fields.Date.today)
    dias_alquiler = fields.Integer(string='Días de alquiler', default=1)
    fecha_devolucion_prevista = fields.Date(
        string='Fecha de devolución prevista',
        compute='_compute_fecha_devolucion_prevista',
    )

    @api.depends('fecha_alquiler', 'dias_alquiler')
    def _compute_fecha_devolucion_prevista(self):
        for record in self:
            if record.dias_alquiler <= 0:
                raise ValidationError(
                    "La duración del alquiler debe ser de al menos un día."
                )

            if record.fecha_alquiler:
                record.fecha_devolucion_prevista = (
                    record.fecha_alquiler + timedelta(days=record.dias_alquiler)
                )
            else:
                record.fecha_devolucion_prevista = False

    @api.constrains('fecha_devolucion','fecha_alquiler')
    def _check_fecha_devolucion(self):
        for record in self:
             if record.fecha_devolucion and record.fecha_alquiler:
                dia_devolucion = record.fecha_devolucion.date()
                if dia_devolucion < record.fecha_alquiler:
                    raise ValidationError(
                        "La fecha de devolución no puede ser anterior a la fecha de alquiler.")
            
    @api.onchange('material_id')
    def _onchange_material_id(self):
        if self.material_id:
            total_precio = sum(material.precio_alquiler for material in self.material_id)
            self.precio_total = total_precio
        else:
            self.precio_total = 0.0

    @api.constrains('material_id', 'fecha_alquiler')
    def _check_material_apto(self):
        for alquiler in self:
            for pieza in alquiler.material_id:
                if pieza.actividad != 'disponible':
                    raise ValidationError(
                        f"La pieza {pieza.display_name} no está disponible."
                    )

                revisiones = pieza.revision_ids.filtered('fecha_revision')
                if not revisiones:
                    raise ValidationError(
                        f"La pieza {pieza.display_name} no tiene una revisión con fecha."
                    )
