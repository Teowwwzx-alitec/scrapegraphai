# Odoo Structure Analysis

**Analysis of Odoo Page Structure**

---

### **Navigation Bar (Navbar)**
- **Main Navbar Element**:  
  `<nav class="o_main_navbar" data-command-category="disabled">` (Element 17)

#### **Menu Items**:
1. **Home Menu**:  
   - **Element**: `<a href="#" class="o_menu_toggle hasImage">` (Element 18)  
     - **Text**: "Inventory" (brand icon and text)  
     - **Attributes**:  
       - `class="o_menu_toggle hasImage"`  
       - `accesskey="h"`  
       - `title="Home menu"`

2. **Primary Menu Sections**:
   - **Overview**:  
     - **Element**: `<a class="dropdown-item o_nav_entry">` (Element 35)  
       - **Text**: "Overview"  
       - **Attributes**:  
         - `href="#menu_id=197&action=305"`  
         - `data-menu-xmlid="stock.stock_picking_type_menu"`  
         - `data-hotkey="1"`

   - **Operations** (Dropdown):  
     - **Element**: `<button class="dropdown-toggle fw-normal">` (Element 37)  
       - **Text**: "Operations"  
       - **Attributes**:  
         - `data-menu-xmlid="stock.menu_stock_warehouse_mgmt"`  
         - `data-hotkey="2"`

   - **Products** (Dropdown):  
     - **Element**: `<button class="dropdown-toggle fw-normal">` (Element 40)  
       - **Text**: "Products"  
       - **Attributes**:  
         - `data-menu-xmlid="stock.menu_stock_inventory_control"`  
         - `data-hotkey="3"`

   - **Reporting** (Dropdown):  
     - **Element**: `<button class="dropdown-toggle fw-normal">` (Element 43)  
       - **Text**: "Reporting"  
       - **Attributes**:  
         - `data-menu-xmlid="stock.menu_warehouse_report"`  
         - `data-hotkey="4"`

   - **Configuration** (Dropdown):  
     - **Element**: `<button class="dropdown-toggle fw-normal">` (Element 46)  
       - **Text**: "Configuration"  
       - **Attributes**:  
         - `data-menu-xmlid="stock.menu_stock_config_settings"`  
         - `data-hotkey="5"`

#### **Systray (Right Side)**:
- **Messages**:  
  - **Element**: `<div class="o-dropdown dropdown o-mail-DiscussSystray-class">` (Element 52)  
    - **Text**: "Messages" (icon with badge "2")  
    - **Class**: `fa fa-comments`

- **Activities**:  
  - **Element**: `<div class="o-dropdown dropdown o-mail-DiscussSystray-class">` (Element 57)  
    - **Text**: "Activities" (icon)  
    - **Class**: `fa fa-clock-o`

- **User Menu**:  
  - **Element**: `<div class="o-dropdown dropdown o_user_menu">` (Element 65)  
    - **Text**: "Administrator" (with avatar and database name "zhenxiang")  
    - **Class**: `o_user_avatar`

---

### **Control Panel**
- **Main Control Panel**:  
  `<div class="o_control_panel">` (Element 73)

#### **Components**:
1. **Breadcrumbs**:  
   - **Element**: `<div class="o_breadcrumb">` (inside Element 75)  
     - **Text**: "Products" (current page).

2. **Action Buttons**:  
   - **New Button**:  
     - **Element**: `<button class="btn btn-primary o-kanban-button-new">` (Element 78)  
       - **Text**: "New"  
       - **Attributes**:  
         - `accesskey="c"`  
         - `data-hotkey="c"`

3. **Search Bar**:  
   - **Element**: `<input class="o_searchview_input">` (inside Element 74)  
     - **Class**: `o_searchview_input`  
     - **Placeholder**: "Search..."  
     - **Hotkey**: `accesskey="Q"`

4. **Pagination**:  
   - **Previous/Next Buttons**:  
     - **Element**: `<button class="o_pager_previous">` and `<button class="o_pager_next">` (inside Element 75)  
       - **Hotkeys**: `p` (previous), `n` (next)  
       - **Disabled**: Both are disabled (only 1 record).

5. **View Switcher**:  
   - **Kanban/List Toggle**:  
     - **Element**: `<nav class="o_cp_switch_buttons">` (inside Element 74)  
       - **Active View**: Kanban (`o_kanban active`).

---

### **Main Panel**
- **View Type**: **Kanban** (class `o_kanban_renderer` in Element 72).

#### **Records**:
1. **Product Record**:  
   - **Element**: `<div class="o_kanban_record" data-id="datapoint_2">` (Element 72)  
     - **Fields**:  
       - **Name**: "test"  
       - **Price**: "$ 1.00"  
       - **Stock**: "On hand: 0.00 Units"  
     - **Actionable Elements**:  
       - **Favorite Star**: `<a class="o_priority_star fa fa-star-o">` (clickable but unselected).

2. **Ghost Records**:  
   - Empty placeholders (`o_kanban_ghost`) for additional items.

---

### **Summary**
This is an **Inventory module** page in Odoo, displaying products in a **Kanban view**. The navbar provides access to inventory sections (Overview, Operations, Products, etc.), while the control panel includes search, pagination, and a "New" button. The main panel shows a single product ("test") with basic details. The user is logged in as "Administrator" with system privileges.