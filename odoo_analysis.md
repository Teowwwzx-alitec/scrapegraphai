# Odoo Structure Analysis

```markdown
### Odoo XML/HTML Structure Analysis

#### 1. Core Application Components
**Menus**:
- Root menu: `stock.menu_stock_root` (Inventory)
- Submenus: 
  - `stock.stock_picking_type_menu` (Overview)
  - `stock.menu_stock_warehouse_mgmt` (Operations)
  - `stock.menu_stock_inventory_control` (Products)
  - `stock.menu_warehouse_report` (Reporting)
  - `stock.menu_stock_config_settings` (Configuration)

**Views**:
- Kanban View: `o_kanban_view` for stock operations (Receipts/Delivery Orders)
- Dashboard layout: `o_kanban_dashboard` with cards showing actionable metrics
- Search view: `o_searchview` with input field and filters

**Templates**:
- Web client base template (`o_web_client` body class)
- Navigation bar template (`o_main_navbar`)
- Kanban card template (`o_kanban_record` with `stock_picking` context)

---

#### 2. Actionable Elements
**Buttons**:
- Process buttons: 
  ```html
  <button name="get_action_picking_tree_ready" type="object">0 To Process</button>
  ```
- Navigation: 
  ```html
  <button data-hotkey="h" title="Home Menu"> (App switcher)
  ```
- Pager controls: 
  ```html
  <button class="o_pager_previous" data-hotkey="p"> (Disabled navigation)
  ```

**Links**:
- Menu navigation: 
  ```html
  <a href="#menu_id=181&action=370" data-menu-xmlid="stock.menu_stock_root">
  ```

**Form Inputs**:
- Global search: 
  ```html
  <input type="text" class="o_searchview_input" accesskey="Q">
  ```

---

#### 3. Business Logic Indicators
**Model References**:
- `stock.picking` model: 
  ```html
  <div name="stock_picking" class="oe_kanban_color_0">
  ```

**Actions**:
- Kanban actions: 
  ```html
  <a name="get_stock_picking_action_picking_type" type="object">
  <button name="get_action_picking_tree_ready" type="object">
  ```
- Controller endpoints: 
  ```javascript
  odoo.reloadMenus = () => fetch(`/web/webclient/load_menus/...`)
  ```

---

#### 4. Inheritance Points
**XPath Targets**:
- Menu structure: 
  ```html
  <nav class="o_main_navbar" data-command-category="disabled"> (Potential extension point)
  ```
- Kanban layout: 
  ```html
  <div class="o_kanban_renderer"> (Common extension target for kanban customizations)
  ```

**CSS Classes**:
- `o_kanban_primary_left/o_kanban_primary_right` (Positional hooks for card content)
- `o_control_panel_main_buttons` (Action button container for extensions)

---

#### 5. Security & Access Control
**Session Data**:
- Admin privileges: 
  ```javascript
  odoo.__session_info__.is_system = true, is_admin = true
  ```
- DB access: 
  ```javascript
  odoo.__session_info__.db = "odoo17_db"
  ```

**Visibility Controls**:
- Conditional rendering: 
  ```html
  <div class="d-none d-md-flex"> (Responsive visibility)
  ```
- Access-key restricted elements: 
  ```html
  <input accesskey="Q"> (Quick search shortcut)
  ```

**CSRF Protection**:
- Token inclusion: 
  ```javascript
  odoo.csrf_token = "bf2e702b87e3978eab832f3f9459f1ddf2571131o1774092620"
  ```
```