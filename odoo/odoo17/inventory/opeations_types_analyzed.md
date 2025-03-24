# Odoo Structure Analysis

**Navigation Bar (Navbar):**
- **Main Navbar Element**: `<nav class="o_main_navbar" data-command-category="disabled">` (Element 17).
- **Menu Items**:
  1. **Overview** (Direct Link)
     - Text: "Overview"
     - Class: `dropdown-item o_nav_entry`
     - Attributes: `href="#menu_id=197&action=305"`, `data-hotkey="1"`, `data-menu-xmlid="stock.stock_picking_type_menu"`.
  2. **Operations** (Dropdown)
     - Text: "Operations"
     - Class: `dropdown-toggle fw-normal`
     - Attributes: `data-hotkey="2"`, `data-menu-xmlid="stock.menu_stock_warehouse_mgmt`.
  3. **Products** (Dropdown)
     - Text: "Products"
     - Class: `dropdown-toggle fw-normal`
     - Attributes: `data-hotkey="3"`, `data-menu-xmlid="stock.menu_stock_inventory_control`.
  4. **Reporting** (Dropdown)
     - Text: "Reporting"
     - Class: `dropdown-toggle fw-normal`
     - Attributes: `data-hotkey="4"`, `data-menu-xmlid="stock.menu_warehouse_report`.
  5. **Configuration** (Dropdown)
     - Text: "Configuration"
     - Class: `dropdown-toggle fw-normal`
     - Attributes: `data-hotkey="5"`, `data-menu-xmlid="stock.menu_stock_config_settings`.

- **Systray Components**:
  - **Messages**: `<i class="fa fa-lg fa-comments">` with badge "2" (Element 52).
  - **Activities**: `<i class="fa fa-lg fa-clock-o">` (Element 57).
  - **User Menu**: Avatar image and username "Administrator" (Element 65).

---

**Control Panel**:
- **Main Control Panel Element**: `<div class="o_control_panel">` (Element 73).
- **Breadcrumbs**:
  - Current Page: "Operations Types" (Element 75).
- **Action Buttons**:
  - **New**: `<button class="btn btn-primary o_list_button_add">` with `data-hotkey="c"`.
  - **Actions Menu**: `<i class="fa fa-cog">` with `data-hotkey="u"`.
- **Search Bar**:
  - Input: `<input class="o_searchview_input">` with `placeholder="Search..."` and `accesskey="Q"`.
  - Toggle: `<i class="fa fa-caret-down">` with `data-hotkey="shift+q"`.
- **Pagination**:
  - Previous/Next: Buttons with classes `o_pager_previous`/`o_pager_next`, both disabled.
  - Counter: "1-2 / 2".

---

**Main Panel**:
- **View Type**: List View (`<div class="o_list_view">` in Element 72).
- **Records**:
  1. **Receipts**
     - `data-id="datapoint_2"`
     - Key Field: "Receipts" (Operation Type).
  2. **Delivery Orders**
     - `data-id="datapoint_3"`
     - Key Field: "Delivery Orders" (Operation Type).
- **Actionable Elements**:
  - Drag handles (`<span class="oi oi-draggable">`) for reordering.
  - Checkboxes for record selection.

---

### Summary of Page Structure:
This is an **Odoo Inventory Management** interface. The navbar provides access to core modules (Overview, Operations, Products, Reporting, Configuration), while the control panel includes a "New" button, search bar, and pagination for managing records. The main panel displays a **list of operation types** (e.g., Receipts, Delivery Orders) in a draggable/sortable table. The user is logged in as "Administrator" with quick access to messages and activities.