# Odoo Structure Analysis

**Navigation Bar (Navbar) Analysis:**
- **Main Navbar Element:** `<nav class="o_main_navbar">` (Element 17)
- **Menu Items:**
  1. **Overview**  
     - Type: Direct link (`<a>` tag)  
     - Attributes: `data-menu-xmlid="stock.stock_picking_type_menu"`, `href="#menu_id=197&action=305"`, `data-hotkey="1"`
  2. **Operations**  
     - Type: Dropdown menu (triggered by `<button>`)  
     - Attributes: `data-menu-xmlid="stock.menu_stock_warehouse_mg""`, `data-hotkey="2"`
  3. **Products**  
     - Type: Dropdown menu  
     - Attributes: `data-menu-xmlid="stock.menu_stock_inventory_control"`, `data-hotkey="3"`
  4. **Reporting**  
     - Type: Dropdown menu  
     - Attributes: `data-menu-xmlid="stock.menu_warehouse_report"`, `data-hotkey="4"`
  5. **Configuration**  
     - Type: Dropdown menu  
     - Attributes: `data-menu-xmlid="stock.menu_stock_config_settings"`, `data-hotkey="5"`

**Control Panel Analysis:**
- **Control Panel Element:** `<div class="o_control_panel">` (Element 73)
- **Components:**
  - **Breadcrumbs:** "Moves History" (in `<div class="o_breadcrumb">`)
  - **Search Bar:**  
    - Input field: `<input class="o_searchview_input">` with placeholder "Search..."  
    - Toggle button: `<i class="fa fa-caret-down" data-hotkey="shift+q">`
  - **Action Buttons:**  
    - Settings cog: `<i class="fa fa-cog" data-hotkey="u">`
  - **View Switchers:**  
    - Buttons for **List** (active), **Kanban**, and **Pivot** views.

**Main Panel Analysis:**
- **Main Panel Element:** `<div class="o_list_view">` (Element 72)
- **View Type:** **List View** (class `o_list_renderer`)
- **Structure:**  
  - Table headers: Date, Reference, Product, From, To, Quantity, Status.  
  - Empty state message: "There's no product move yet" with instructions about filtering product movements.

**Key Observations:**
1. The page belongs to the **Inventory** module (navbar branding shows "Inventory").
2. The user is viewing the **Moves History** list (breadcrumb), which tracks product movements.
3. The list is currently empty, suggesting no inventory moves exist or match the applied filters.
4. Navigation hotkeys are heavily integrated (e.g., `1-5` for menus, `shift+q` for search, `u` for actions).
5. The interface supports multiple views (List/Kanban/Pivot) but defaults to a list view.