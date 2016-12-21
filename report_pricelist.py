
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

from datetime import datetime , timedelta 
from dateutil import parser

from openerp import models, fields, api ,  SUPERUSER_ID
from openerp import tools


from openerp.tools.translate import _
import re
import logging

import requests
from lxml import etree

_logger = logging.getLogger(__name__) 



class saved_price_list(models.Model):

    _name = 'saved.price_list'
    _description = 'saved Price List'


    name = fields.Char()



    price_list = fields.Many2one('product.pricelist', 'PriceList', required=True)
    category_ids = fields.Many2many('product.category','saved_pricelist_products_rel','list_id','product_id','Categorias')
    supplier_ids = fields.Many2many('res.partner','saved_pricelist_supplier_rel','list_id','suplier_id','Vendedor')
    has_image = fields.Boolean('Solo con imagen')
    has_stock = fields.Boolean('Solo con stock')


    qty1 = fields.Integer('Cantidad 1' , default=1)
    qty2 = fields.Integer('Cantidad 2' , default=0)
    qty3 = fields.Integer('Cantidad 3' , default=0)
    qty4 = fields.Integer('Cantidad 4' , default=0)
    qty5 = fields.Integer('Cantidad 5' , default=0)

    @api.multi
    def print_report(self):

        ids=[]
        categorys = []
        _logger.info('uno %r' ,self.category_ids)
        if self.category_ids : 

            for parent_id in self.category_ids:
                childs = self.env['product.category'].search([('id','child_of',parent_id.id)])
                _logger.info('dos %r ',childs )

                for child in childs:
                    categorys.append(child.id)

            args.append(('categ_id','in',categorys))

        if self.has_image :
            args.append(('image','<>',False)) 

        if self.has_stock :
            args.append(('qty_available','>',1)) 
        
        products_tmpl_ids = self.env['product.template'].search(args)        
        products_tmpl_ids = [ x.id for x in products_tmpl_ids]

        products_ids = self.env['product.product'].search([('product_tmpl_id','in',products_tmpl_ids)])        
        #products=self.env['product.product'].browse(products_ids)

        products_ids = [x.id for x in products_ids]


        data = {                    
                        'model':'product.product',                    
                        'ids': products_ids , 
                        'form' : {
                            'price_list' : self.price_list.id,
                            'qty1' : self.qty1,
                            'qty2' : self.qty2,
                            'qty3' : self.qty3,
                            'qty4' : self.qty4,
                            'qty5' : self.qty5,
                        
                        },                
                        'report_type': 'qweb-pdf',
                        'nodestroy': True
                       }
        
        return {
            'type': 'ir.actions.report.xml',            
            'report_name':'ba_report_pricelist.report_product_product_images',            
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


