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

from datetime import datetime , timedelta ,  date 
from dateutil import parser

from openerp import models, fields, api ,  SUPERUSER_ID
from openerp import tools


from openerp.tools.translate import _
import re
import logging

import requests
from lxml import etree

_logger = logging.getLogger(__name__) 


class product_product(models.Model):
    _inherit = 'product.product'

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



class saved_price_list(models.Model):

    _name = 'saved.price_list'
    _description = 'saved Price List'


    name = fields.Char()



    price_list = fields.Many2one('product.pricelist', 'PriceList', required=True)
    category_ids = fields.Many2many('product.category','saved_pricelist_products_rel','list_id','product_id','Categorias')
    supplier_ids = fields.Many2many('res.partner','saved_pricelist_supplier_rel','list_id','suplier_id','Vendedor')
    has_image = fields.Boolean('Solo con imagen')
    has_stock = fields.Boolean('Solo con stock')
    show_stock = fields.Boolean('Mostrar stock')
    show_tax = fields.Boolean('Totales con impuesto')
    show_supplier = fields.Boolean('Mostar proveedor')
    show_descripcion = fields.Boolean('Mostar Descripcion')
    format = fields.Selection([('list', 'Lista'),('catalog', 'Catalogo'),('twice', 'Ambos')])

    @api.multi
    def print_report(self):

        ids=[]
        categorys = []
        args = []
        if self.category_ids : 

            for parent_id in self.category_ids:
                childs = self.env['product.category'].search([('id','child_of',parent_id.id)])

                for child in childs:
                    categorys.append(child.id)

            args.append(('categ_id','in',categorys))

        if self.supplier_ids:
            supplier_ids = [x.id for x in self.supplier_ids] 
            #supplier_ids = self.env['product.supplierinfo'].search([('name','in',supplier_ids)])
            #supplier_ids = [x.id for x in supplier_ids] 

            args.append(('seller_ids.name','in',supplier_ids))

        if self.has_image :
            args.append(('image','!=',False)) 

        if self.has_stock :
            args.append(('qty_available','>',1)) 

        _logger.info ("args %r", args)

        
        #products_tmpl_ids = self.env['product.template'].search(args)        
        #_logger.info ("products_tmpl_ids %r", products_tmpl_ids)
        #products_tmpl_ids = [ x.id for x in products_tmpl_ids]

        products_ids = self.env['product.product'].search(args,
                order='default_code')        
        #products_ids = self.env['product.product'].search([('product_tmpl_id','in',products_tmpl_ids)],
        #        order='default_code')        
        #products=self.env['product.product'].browse(products_ids)
        _logger.info(self.format)
        products_ids = [x.id for x in products_ids]


        data = {                    
                        'model':'product.product',                    
                        'ids': products_ids , 
                        'form' : {
                            'price_list' : self.price_list.id,
                            'name' : self.name ,
                            'has_image' : self.has_image ,
                            'has_stock' : self.has_stock ,
                            'show_stock' : self.show_stock ,
                            'show_tax' : self.show_tax ,
                            'show_supplier' : self.show_supplier,
                            'show_descripcion' : self.show_descripcion ,
                            'format' : self.format

          
                        
                        },                
                        'report_type': 'qweb-pdf',
                        'nodestroy': False
                       }
        
        return {
            'type': 'ir.actions.report.xml',            
            'report_name':'ba_report_pricelist.report_product_pricelist_images',            
            'datas': data
            }

    def old_print_report(self, cr, uid, ids, context=None):
        """
        To get the date and print the report
        @return : return report
        """
        if context is None:
            context = {}
        datas = {'ids': context.get('active_ids', [])}
        res = self.read(cr, uid, ids, ['price_list','qty1', 'qty2','qty3','qty4','qty5'], context=context)
        res = res and res[0] or {}
        res['price_list'] = res['price_list'][0]
        datas['form'] = res
        return self.pool['report'].get_action(cr, uid, [], 'product.report_pricelist', data=datas, context=context)


