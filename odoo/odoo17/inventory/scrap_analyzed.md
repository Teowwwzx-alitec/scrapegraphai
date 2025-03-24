# Odoo Structure Analysis

**Navigation Bar (Navbar) Analysis**

1. **Main Navbar Element**
   - Element: `<nav class="o_main_navbar">` (Element 17)
   - Components:
     - Home Menu Toggle: `<a class="o_menu_toggle hasImage">` (Element 18) with Inventory branding.
     - Menu Sections: 5 main dropdown menus.

2. **Menu Items**
   - **Overview**
     - Text: "Overview"
     - `data-menu-xmlid`: `stock.stock_picking_type_menu`
     - `href`: `#menu_id=197&action=305`
     - `data-hotkey`: "1"
   - **Operations**
     - Text: "Operations"
     - `data-menu-xmlid`: `stock.menu_stock_warehouse_mgmt`
     - `data-hotkey`: "2"
   - **Products**
     - Text: "Products"
     - `data-menu-xmlid`: `stock.menu_stock_inventory_control`
     - `data-hotkey`: "3"
   - **Reporting**
     - Text: "Reporting"
     - `data-menu-xmlid`: `stock.menu_warehouse_report`
     - `data-hotkey`: "4"
   - **Configuration**
     - Text: "Configuration"
     - `data-menu-xmlid`: `stock.menu_stock_config_settings`
     - `data-hotkey`: "5"

3. **Systray Components**
   - Messages: Button with counter "2" (Element 53).
   - Activities: Button with clock icon (Element 58).
   - User Menu: Displays user avatar and database name "zhenxiang" (Element 66).

---

**Control Panel Analysis**

1. **Main Control Panel**
   - Element: `<div class="o_control_panel">` (Element 73)

2. **Components**
   - **Breadcrumbs**
     - Current Page: "Scrap Orders" (Element 75).
   - **Action Buttons**
     - "New" Button: `<button class="btn btn-primary o_list_button_add">` with `data-hotkey="c"`.
   - **Search Bar**
     - Input: `<input class="o_searchview_input">` with `accesskey="Q"`.
   - **Pagination**
     - Previous/Next buttons (both disabled).
     - Counter: "1-1 / 1".
   - **View Switcher**
     - Active View: List view (`o_list`).
     - Other Options: Kanban, Pivot, Graph.

---

**Main Panel Analysis**

1. **View Type**
   - **List View**: `<div class="o_list_renderer">` (Element 72).

2. **Records/Items**
   - Single record with:
     - `data-id`: "datapoint_2"
     - Fields:
       - Reference: "New"
       - Product: "test"
       - Quantity: 1.00
       - Status: "Draft" (badge)

---

**Additional Observations**
- The page title is "Odoo - Scrap Orders".
- User is logged in as "Administrator" with database "zhenxiang".
- Two unread messages in the messaging systray.
- The scrap order list shows one draft record with minimal details.

---

**Summary**
This is an **Inventory Management** interface in Odoo, focused on **Scrap Orders**. The user is viewing a list of scrap orders in list-view format, with one draft entry. The navbar provides access to inventory operations, products, reporting, and configuration. The control panel allows record creation (`New`), search, and view switching. The single scrap order is in draft state with basic product information.