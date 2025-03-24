# Odoo Structure Analysis

**Navigation Bar (Navbar) Analysis:**
1. **Main Navbar Element:**  
   - Found in Element 17: `<nav class="o_main_navbar" ...>`

2. **Menu Items & Submenus:**  
   - **Overview** (Direct Link):  
     - Text: "Overview"  
     - `data-menu-xmlid`: `stock.stock_picking_type_menu`  
     - `href`: `#menu_id=197&action=305`  
     - `data-hotkey`: "1"  

   - **Operations** (Dropdown):  
     - Text: "Operations"  
     - `data-menu-xmlid`: `stock.menu_stock_warehouse_mgmt`  
     - `data-hotkey`: "2"  

   - **Products** (Dropdown):  
     - Text: "Products"  
     - `data-menu-xmlid`: `stock.menu_stock_inventory_control`  
     - `data-hotkey`: "3"  

   - **Reporting** (Dropdown):  
     - Text: "Reporting"  
     - `data-menu-xmlid`: `stock.menu_warehouse_report`  
     - `data-hotkey`: "4"  

   - **Configuration** (Dropdown):  
     - Text: "Configuration"  
     - `data-menu-xmlid`: `stock.menu_stock_config_settings`  
     - `data-hotkey`: "5"  

3. **User Menu & System Tray:**  
   - **Messages**: Icon with badge "2" (Element 52).  
   - **Activities**: Clock icon (Element 57).  
   - **User Profile**: Avatar + "Administrator" (Element 65).  

---

**Control Panel Analysis:**
1. **Main Control Panel Element:**  
   - Found in Element 73: `<div class="o_control_panel ...">`

2. **Key Components:**  
   - **Breadcrumbs**: "Stock" (Element 75).  
   - **Search Bar**:  
     - Input field with `class="o_searchview_input"` (Element 74).  
     - Hotkey: `accesskey="Q"`.  
   - **Action Buttons**:  
     - "New" button with `data-hotkey="c"` (Element 78).  
     - Actions dropdown (⚙️ icon) with `data-hotkey="u"` (Element 75).  
   - **Pagination**:  
     - Previous/Next buttons (disabled) with `data-hotkey="p"` and `data-hotkey="n"` (Element 74).  

---

**Main Panel Analysis:**
1. **View Type**:  
   - **List View** (`o_list_renderer` class in Element 72).  

2. **Records/Items**:  
   - Single record with `data-id="datapoint_2"`:  
     - **Fields**:  
       - Product: "test"  
       - On Hand: 0.00  
       - Free to Use: 0.00  
       - Incoming: 0.00  
       - Outgoing: 0.00  
     - **Action Buttons**:  
       - "Inventory Adjustment" (Pencil icon, `name="277"`).  
       - "History" (`name="286"`).  
       - "Replenishment" (`name="action_view_orderpoints"`).  

---

**Summary of Page Structure:**  
This is an **Inventory Management** interface in Odoo. The navbar provides access to core inventory modules (Operations, Products, Reporting, Configuration). The control panel includes search, creation ("New" button), and navigation tools. The main panel displays a **List View** of products with stock metrics (On Hand, Free to Use, etc.) and actionable buttons for adjustments. The user is logged in as "Administrator" with access to messaging and activity tracking.