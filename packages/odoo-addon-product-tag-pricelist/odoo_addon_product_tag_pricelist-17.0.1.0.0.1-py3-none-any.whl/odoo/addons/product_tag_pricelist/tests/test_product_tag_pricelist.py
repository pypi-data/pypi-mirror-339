# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProductTagPricelist(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create products, pricelist, partner and empty sale
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.categ = cls.env["product.category"].create({"name": "Test Categ"})
        cls.tag = cls.env["product.tag"].create({"name": "Test Tag"})
        cls.product1 = cls.env["product.product"].create(
            {"name": "Test Product 1", "additional_product_tag_ids": [(4, cls.tag.id)]}
        )
        cls.product2 = cls.env["product.product"].create(
            {
                "name": "Test Product 2",
                "categ_id": cls.categ.id,
            }
        )
        cls.product3 = cls.env["product.product"].create(
            {
                "name": "Test Product 3",
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Test Pricelist",
            }
        )
        cls.line1 = cls.pricelist.item_ids.create(
            {
                "compute_price": "fixed",
                "fixed_price": 1.0,
                "applied_on": "3_global",
            }
        )
        cls.line2 = cls.pricelist.item_ids.create(
            {
                "compute_price": "fixed",
                "fixed_price": 10.0,
                "applied_on": "2a_product_tags",
                "product_tag_ids": [(4, cls.tag.id)],
            }
        )
        cls.line3 = cls.pricelist.item_ids.create(
            {
                "compute_price": "fixed",
                "fixed_price": 100.0,
                "applied_on": "2_product_category",
                "categ_id": cls.categ.id,
            }
        )

    def test_pricelist(self):
        price1 = self.pricelist._get_product_price(self.product1, quantity=1.0)
        price2 = self.pricelist._get_product_price(self.product2, quantity=1.0)
        price3 = self.pricelist._get_product_price(self.product3, quantity=1.0)

        self.assertEqual(price1, 10)
        self.assertEqual(price2, 100)
        self.assertEqual(price3, 1)

    def test_check_product_consistency(self):
        with self.assertRaises(ValidationError):
            self.pricelist.item_ids.create(
                {
                    "compute_price": "fixed",
                    "fixed_price": 10.0,
                    "applied_on": "2a_product_tags",
                }
            )

    def test_name(self):
        self.line2._compute_name_and_price()
        self.assertEqual(self.line2.name, f"Tags: {self.tag.name}")

    def test_write_create(self):
        self.line2.write(
            {
                "applied_on": "3_global",
            }
        )
        self.assertEqual(len(self.line2.product_tag_ids), 0)
        self.line3.write(
            {
                "applied_on": "2a_product_tags",
                "product_tag_ids": [(4, self.tag.id)],
            }
        )
        self.assertEqual(len(self.line3.categ_id), 0)
        line4 = self.pricelist.item_ids.create(
            {
                "compute_price": "fixed",
                "fixed_price": 1.0,
                "applied_on": "3_global",
                "product_tag_ids": [(4, self.tag.id)],
            }
        )
        self.assertEqual(len(line4.product_tag_ids), 0)
        line5 = self.pricelist.item_ids.create(
            {
                "compute_price": "fixed",
                "fixed_price": 1.0,
                "applied_on": "2a_product_tags",
                "product_tag_ids": [(4, self.tag.id)],
                "categ_id": self.categ.id,
            }
        )
        self.assertEqual(len(line5.categ_id), 0)
        line6 = self.pricelist.item_ids.create(
            {
                "compute_price": "fixed",
                "fixed_price": 1.0,
                "product_tag_ids": [(4, self.tag.id)],
            }
        )
        self.assertEqual(line6.applied_on, "2a_product_tags")

    def test_onchange(self):
        tag2 = self.env["product.tag"].create({"name": "Test Tag 2"})
        self.product1.product_tag_ids = tag2
        res = self.product1._onchange_tag_ids()
        self.assertEqual(type(res), dict)
        self.assertTrue(res["warning"])

        self.product1.product_tmpl_id.product_tag_ids = tag2
        res = self.product1.product_tmpl_id._onchange_tag_ids()
        self.assertEqual(type(res), dict)
        self.assertTrue(res["warning"])
