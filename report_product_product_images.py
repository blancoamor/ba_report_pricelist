# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import api, models

class report_product_catalog_images(models.AbstractModel):
    _name = 'report.ba_report_pricelist.report_product_catalog_images'
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']

        report = report_obj._get_report_from_name('ba_report_pricelist.report_product_catalog_images')
        docargs = {
            'doc_ids': self._ids,
            'form': data['form'],
            'doc_model': report.model,
            'docs': self.env['product.product'].browse(self._ids),
        }
        return report_obj.render('ba_report_pricelist.report_product_catalog_images', docargs)  



class report_product_pricelist_images(models.AbstractModel):
    _name = 'report.ba_report_pricelist.report_product_pricelist_images'
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']

        report = report_obj._get_report_from_name('ba_report_pricelist.report_product_pricelist_images')
        docargs = {
            'doc_ids': self._ids,
            'form': data['form'],
            'doc_model': report.model,
            'docs': self.env['product.product'].browse(self._ids),
        }
        return report_obj.render('ba_report_pricelist.report_product_pricelist_images', docargs)  

    def _get_price(self, pricelist_id, product_id, qty,tax):
        if (tax):
            tax = 1.21
        else :            
            tax = 1

        pricelist_obj =  self.pool.get('product.pricelist')
        return pricelist_obj.price_get(
                self._cr, self._uid, [pricelist_id],
                product_id, 1.0,
                1, {
                    'uom': 1,
                })[pricelist_id] * tax




"""
class product_product_images_parser(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):
        super(product_product_images_parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            '_get_price': self._get_price,
        })

    def _get_price(self, pricelist_id, product_id):
        qty = 1
        sale_price_digits = self.get_digits(dp='Product Price')
        pricelist = self.pool.get('product.pricelist').browse(self.cr, self.uid, [pricelist_id], context=self.localcontext)[0]
        price_dict = self.pool.get('product.pricelist').price_get(self.cr, self.uid, [pricelist_id], product_id, qty, context=self.localcontext)
        if price_dict[pricelist_id]:
            price = self.formatLang(price_dict[pricelist_id], digits=sale_price_digits, currency_obj=pricelist.currency_id)
        else:
            res = self.pool.get('product.product').read(self.cr, self.uid, [product_id])
            price =  self.formatLang(res[0]['list_price'], digits=sale_price_digits, currency_obj=pricelist.currency_id)
        return price




class report_images_parser(models.AbstractModel):
    _name = 'report.ba_report_pricelist.report_product_pricelist_images'
    _inherit = 'report.abstract_report'
    _template = 'ba_report_pricelist.report_product_pricelist_images'
    _wrapped_report_class = product_product_images_parser

"""