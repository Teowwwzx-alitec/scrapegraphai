# Odoo Structure Analysis

**Navigation Bar (Navbar):**  
- Located in Element 16 (`<nav class="o_main_navbar">`).  
- **Menu Items**:  
  1. **Overview**  
     - Text: "Overview"  
     - `data-menu-xmlid`: `stock.stock_picking_type_menu`  
     - `href`: `#menu_id=197&action=305`  
     - `data-hotkey`: "1"  
  2. **Operations** (Dropdown)  
     - Text: "Operations"  
     - `data-menu-xmlid`: `stock.menu_stock_warehouse_mgmt`  
     - `data-hotkey`: "2"  
  3. **Products** (Dropdown)  
     - Text: "Products"  
     - `data-menu-xmlid`: `stock.menu_stock_inventory_control`  
     - `data-hotkey`: "3"  
  4. **Reporting** (Dropdown)  
     - Text: "Reporting"  
     - `data-menu-xmlid`: `stock.menu_warehouse_report`  
     - `data-hotkey`: "4"  
  5. **Configuration** (Dropdown)  
     - Text: "Configuration"  
     - `data-menu-xmlid`: `stock.menu_stock_config_settings`  
     - `data-hotkey`: "5"  

- **Systray Components**:  
  - Messages (with counter "2") and Activities icons.  
  - User menu with avatar, username "Administrator", and database "zhenxiang".  

---

**Control Panel**:  
- Located in Element 73 (`<div class="o_control_panel">`).  
- **Breadcrumbs**:  
  - Current page: "Move Analysis" (Element 75).  
- **Search Bar**:  
  - Input field with `class="o_searchview_input"` and placeholder "Search...".  
  - Filter: "Done" with a remove button.  
  - Hotkey: `accesskey="Q"` and `data-hotkey="shift+q"`.  
- **Action Buttons**:  
  - Settings cog icon (`data-hotkey="u"`).  
  - View switchers: **Pivot** (active), List, Graph, Kanban.  

---

**Main Panel**:  
- **View Type**: Pivot Table (`class="o_pivot_view"`).  
- **Data Structure**:  
  - Columns: "Demand" and "Count" aggregated by Operation Types (e.g., "Laoreet id", "Volutpat blandit").  
  - Rows: Dates (e.g., "February 2025", "March 2025") with numerical values.  
  - Example Record:  
    - Total Demand: 892.95  
    - Total Count: 16  
- **Empty State**:  
  - Message: "No stock move found" with instructions to filter by product.  

---

**Summary**:  
This is an **Inventory Move Analysis** page in Odoo. The navbar shows navigation for Inventory management, the control panel allows searching/filtering and switching views, and the main panel displays a pivot table analyzing stock moves. The data appears to be sample/placeholder (e.g., "Laoreet id" as a placeholder operation type), and the interface is tailored for tracking inventory operations with metrics like "Demand" and "Count".