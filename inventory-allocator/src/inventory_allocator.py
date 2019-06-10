class InventoryAllocator:
  def __init__(self, order, inventoryDist):
    # Initialize the class with the given arguments
    # Add total count of items from the order 
    # to check if all items were available for shipment
    self.order = order
    self.inventoryDist = inventoryDist
    self.total_order_count = sum(order.values())
  
  def check_warehouse_for_order(self, order, wh_inventory):
    # Total shipment information for the current warehouse
    warehouse_shipments = {}
    
    for wh_item in wh_inventory:
      # Count of of the current item in this warehouse
      wh_item_quantity = wh_inventory[wh_item]
      
      # Skip this item if the count is 0
      if wh_item_quantity == 0: 
        continue
      
      # Only process the item if it is in the order
      if wh_item in order:
        # Shows the count of the item in the order
        order_item_quantity = order[wh_item]

        if wh_item_quantity >= order_item_quantity:
          # If warehouse has more items than needed
          # Just ship as many as in the order 
          warehouse_shipments[wh_item] = order_item_quantity
          self.total_order_count -= order_item_quantity
          del self.order[wh_item]
        else:
          # Otherwise, ship as many as available in the warehouse
          self.order[wh_item] -= wh_item_quantity
          self.total_order_count -= wh_item_quantity
          warehouse_shipments[wh_item] = wh_item_quantity

    return warehouse_shipments

  def find_cheapest_shipment_option(self):
    cheapest_shipment_options = []
   
    for warehouse in self.inventoryDist:
      # For each inventory check if it has items from the order
      # and if so, ship as many as available
      wh_name, wh_inventory = warehouse['name'], warehouse['inventory']
      curr_warehouse_shipments = self.check_warehouse_for_order(self.order, wh_inventory)
      
      # If current warehouse doesn't have items from the order
      # continue with other warehouses
      if not bool(curr_warehouse_shipments):
        continue

      # Otherwise, add the current shipment summary
      # to the final result list
      curr_shipment_summary = { wh_name: curr_warehouse_shipments }
      cheapest_shipment_options.append(curr_shipment_summary)
   
    # Some items were not in any of the warehouses
    # Cancel the order instead
    if self.total_order_count > 0:
      return []

    return cheapest_shipment_options
