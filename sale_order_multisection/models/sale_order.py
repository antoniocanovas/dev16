from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SaleOrderSets(models.Model):
    _inherit = 'sale.order'


    @api.depends('partner_id')
    def get_key(self):
        for record in self:
            key = "$"
            reg = self.env['ir.config_parameter'].sudo().search([('key', '=', 'multisection_key')])
            if reg.id: key = reg.value
            if record.multisection_key: key = record.multisection_key
            record['multisection_key'] = key

    multisection_key = fields.Char('Multisection Key', compute=get_key, readonly=False, required=True)

    def _get_lines_count(self):
        for record in self:
            total = 0
            results = self.env['sale.order.line'].search([
                ('order_id', '=', record.id),
                ('display_type', '=', 'line_section')])
            if results: total = len(results)
            record['section_line_count'] = total

    section_line_count = fields.Integer('Lines', compute=_get_lines_count)

    def action_view_sections(self):
        action = self.env.ref(
            'sale_order_multisection.action_view_sections').read()[0]
        return action

    # Sobra (8/2023) ya lo hace update_multisection:
#    def order_sections(self):
        # Reorder sections and lines by section:
        #        sections = self.env['sale.order.line'].search(
        #    [('order_id', '=', self.id), ('display_type', '=', 'line_section')]).sorted(key=lambda r: r.section)
        #lineas, counter = [], 0
        # Previous lines with no section:
        #lines_no_section = self.env['sale.order.line'].search(
        #    [('order_id', '=', self.id), ('section_id', '=', False), ('display_type', '!=', 'line_section')])
        #for li in lines_no_section:
        #    if li.sequence > counter: counter = li.sequence
        #counter = counter + 1
        # Ordering sections:
        #for se in sections:
        #    for li in self.order_line:
        #        if (li.id == se.id) or (li.section_id.id == se.id):
        #            lineas.append(li)
        # New sequence to array lines:
        #for li in lineas:
        #    li['sequence'] = counter
    #    counter += 1

    def update_multisection(self):
        for record in self:
            # Authomated Actions if section_ids and 'draft' status:
            section_ids = self.env['sale.order.line'].search(
                [('order_id', '=', record.id), ('display_type', '=', 'line_section')])
            if (section_ids) and (record.state == 'draft'):
                line_ids = record.order_line.sorted(key=lambda r: r.sequence)
                section_id, i = 0, 1

#  Hay que asignar 'section' lo hacemos en el momento de crear la línea (ver sol):
                # Set 'section' in section lines and 'section_id' in others, ordered by sequence:
#                for li in section_ids:
#                    section_id = li.id
#                    section_code = str(li.sequence)
#                    if (li.name[:1] == record.multisection_key):
#                        section_code = li.name.split()[0]
#                    li.write({'section': section_code})
# --------- hasta aquí lo anterior

                # Cases products and notes:
                # (da igual secuencia porque utilizaré el nuevo indice ms_sequence)
                section_id = 0
                for li in line_ids:
                    if li.display_type == 'line_section':
                        section_id = li.id
                    else:
                        if (li.new_section_id.id):
                            value = li.new_section_id.id
                        elif (section_id != 0) and not (li.new_section_id.id):
                            value = section_id
                        else:
                            value = False
                        li.write({'section_id': value})

                # Reordenar secuencias para líneas de new_section_id:
                lines = record.order_line.sorted(key=lambda r: r.ms_sequence)
                #    raise UserError(lines)
                for li in lines:
                    li.write({'sequence': i, 'new_section_id': False})
                    i += 1

                # Cálculo de 'parent_ids', 'child_ids' y 'level' por sección, si hay multinivel ($ o multisection_key):
                section_ids = self.env['sale.order.line'].search([('order_id', '=', record.id), ('display_type', '=', 'line_section')])
                for se in section_ids:
                    parents, children, level = [], [], 1
                    line_ids = self.env['sale.order.line'].search(
                        [('order_id', '=', record.id), ('display_type', '=', 'line_section'), ('id', '!=', se.id)])
                    if (se.name[:1] == record.multisection_key):
                        for li in line_ids:
                            lenght_line = len(li.section)
                            if (li.section == se.section[:lenght_line]):
                                parents.append(li.id)
                                level = len(parents) + 1
                            lenght_section = len(se.section)
                            if (se.section == li.section[:lenght_section]):
                                children.append(li.id)
                    se.write({'parent_ids': [(6, 0, parents)], 'child_ids': [(6, 0, children)], 'level': level})
