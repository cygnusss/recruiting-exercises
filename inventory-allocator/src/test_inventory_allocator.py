import unittest
from inventory_allocator import InventoryAllocator

'''
NOTE: Just want to point out that I decided not to cover input validation 
(like if order is a dictionary, if it's not empty etc..) both here in the tests and in the actual code
for the sake of readibility (and I wasn't sure if it would be necessary) 
'''

class TestInventoryAllocator(unittest.TestCase):
  # The following tests test the check_warehouse_for_order method
  def test_single_wh_sufficient(self):
    order = { 'apple': 1 }
    warehouses = [{ 'name': 'owd', 'inventory': { 'apple': 1 } }]
    inventory ={ 'apple': 1 }
    inv_alloc = InventoryAllocator(order, warehouses)
    actual = inv_alloc.check_warehouse_for_order(order, inventory)
    expected = { 'apple': 1 }
    self.assertEqual(actual, expected, 'SOMETHING IS WRONG IN: single wh sufficient')

  def test_single_wh_insufficient(self):
    order = { 'apple': 1 }
    warehouses = [{ 'name': 'owd', 'inventory': { 'apple': 0 } }]
    inventory ={ 'apple': 0 }
    inv_alloc = InventoryAllocator(order, warehouses)
    actual = inv_alloc.check_warehouse_for_order(order, inventory)
    expected = {}
    self.assertEqual(actual, expected, 'SOMETHING IS WRONG IN: single wh insufficient')

  def test_single_wh_oversufficient(self):
    order = { 'apple': 1 }
    warehouses = [{ 'name': 'owd', 'inventory': { 'apple': 10000 } }]
    inventory ={ 'apple': 10000 }
    inv_alloc = InventoryAllocator(order, warehouses)
    actual = inv_alloc.check_warehouse_for_order(order, inventory)
    expected = { 'apple': 1 }
    self.assertEqual(actual, expected, 'SOMETHING IS WRONG IN: single wh oversufficient')
  
  # The following tests test the find_cheapest_shipment_option method
  def test_exacc_match(self):
    order = { 'apple': 1 }
    warehouses = [{ 'name': 'owd', 'inventory': { 'apple': 1 } }]
    inv_alloc = InventoryAllocator(order, warehouses)
    actual = inv_alloc.find_cheapest_shipment_option()
    expected = [{ 'owd': { 'apple': 1 } }]    
    self.assertEqual(actual, expected, 'SOMETHING IS WRONG IN: exact match')
  
  def test_no_allocations(self):
    order = { 'apple': 1 }
    warehouses = [{ 'name': 'owd', 'inventory': { 'apple': 0 } }]
    inv_alloc = InventoryAllocator(order, warehouses)
    actual = inv_alloc.find_cheapest_shipment_option()
    expected = []
    self.assertEqual(actual, expected, 'SOMETHING IS WRONG IN: no allocations')

  def test_split_case(self):
    order = { 'apple': 10 }
    warehouses = [{ 'name': 'owd', 'inventory': { 'apple': 5 } }, { 'name': 'dm', 'inventory': { 'apple': 5 }}]
    inv_alloc = InventoryAllocator(order, warehouses)
    actual = inv_alloc.find_cheapest_shipment_option()
    expected = [{ 'owd': { 'apple': 5 }}, { 'dm': { 'apple': 5 } }]
    self.assertEqual(actual, expected, 'SOMETHING IS WRONG IN: split case')

  def test_sufficient_first_wh(self):
    order = { 'apple': 10 }
    warehouses = [{ 'name': 'owd', 'inventory': { 'apple': 5213124124 } }, { 'name': 'dm', 'inventory': { 'apple': 5 }}]
    inv_alloc = InventoryAllocator(order, warehouses)
    actual = inv_alloc.find_cheapest_shipment_option()
    expected = [{ 'owd': { 'apple': 10 }}]
    self.assertEqual(actual, expected, 'SOMETHING IS WRONG IN: sufficient first wh')
    
  def test_sufficient_second_wh(self):
    order = { 'apple': 10 }
    warehouses = [{ 'name': 'owd', 'inventory': { 'apple': 0 } }, { 'name': 'dm', 'inventory': { 'apple': 51337 }}]
    inv_alloc = InventoryAllocator(order, warehouses)
    actual = inv_alloc.find_cheapest_shipment_option()
    expected = [{ 'dm': { 'apple': 10 }}]
    self.assertEqual(actual, expected, 'SOMETHING IS WRONG IN: sufficient second wh')
  
  def test_all_insufficient(self):
    order = { 'apple': 10 }
    warehouses = [{ 'name': 'owd', 'inventory': { 'apple': 4 } }, { 'name': 'dm', 'inventory': { 'apple': 4 }}]
    inv_alloc = InventoryAllocator(order, warehouses)
    actual = inv_alloc.find_cheapest_shipment_option()
    expected = []
    self.assertEqual(actual, expected, 'SOMETHING IS WRONG IN: all sufficient')

if __name__ == '__main__':
  unittest.main()
