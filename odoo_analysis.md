# Odoo Structure Analysis

```markdown
# Odoo XML/HTML Analysis

## 1. Core Application Components

### Menus
- **Main Navigation Menu**:  
  `<nav class="o_main_navbar">` with menu items like "Site", "Reporting", "Configuration" (Elements 34-43)  
  `data-menu-xmlid` attributes reference menu definitions (e.g., `website.menu_site`)

### Views
- **Home Menu Grid**:  
  `<div class="o_apps">` containing application icons (Elements 67-93)  
  Standard Odoo apps: Discuss (`mail.menu_root_discuss`), Contacts (`contacts.menu_contacts`), Website (`website.menu_website_configuration`)

### Templates
- **Notification System**:  
  `<div class="o_notification_manager">` with password security warning (Element 15)  
  Uses Odoo's standard alert template with dismiss functionality

## 2. Actionable Elements

### Buttons
- **Navigation Controls**:  
  `o_menu_toggle` (hamburger menu), `o_mobile_menu_toggle` (mobile menu)  
  `data-hotkey` attributes for keyboard navigation (Elements 36,42)

### Form Inputs
- **Global Search**:  
  `<input class="o_search_hidden">` with ARIA combobox role (Element 69)  
  Implements Odoo's global command palette pattern

### Action Links
- **App Launchers**:  
  `<a data-menu-xmlid="mail.menu_root_discuss" href="#action_id=107">`  
  Triggers window actions through URL hash parameters (standard Odoo navigation)

## 3. Business Logic Indicators

### Model References
- **User Session Data**:  
  `odoo.__session_info__` contains `partner_id`, `user_id`, and company relationships (Element 12)  
  `res.users` model avatar via `/web/image?model=res.users` (Element 63)

### Action Bindings
- **Window Actions**:  
  `href="#menu_id=70&action_id=107"` connects menu items to ir.actions.client (Element 77)  
  `inbox_action: 107` in session info shows action registry usage

## 4. Inheritance Points

### XPath Targets
- **Menu System Extension**:  
  `data-menu-xmlid` attributes provide extension hooks for custom modules  
  Example: `website.menu_website_global_configuration` could be extended via `<xpath expr="//*[@data-menu-xmlid='website.menu_website_global_configuration']">`

### Template Hooks
- **Notification Overrides**:  
  `database_expiration_panel` (Element 71) uses standard Odoo alert markup for customization  
  `o-mail-DiscussSystray-class` indicates discuss module extension points

## 5. Security & Access Control

### Authentication
- **CSRF Protection**:  
  `csrf_token: "063a698036535f2c2e6b222c146c0230948f123bo1774167718"` in header (Element 7)  
  Session validation through `__session_info__.uid`

### Permissions
- **Admin Privileges**:  
  `is_system: true, is_admin: true` in session info (Element 12)  
  `user_companies` structure enforces multi-company security rules

### Access Rules
- **Menu Visibility**:  
  `display_switch_company_menu: false` controls UI elements based on permissions  
  `base.menu_administration` link (Element 93) only visible to admin users

## Key Odoo Technical Insights
1. **Menu-Action Binding**: Uses hash parameters (#menu_id+X+action_id+Y) for client-side routing
2. **Modular CSS**: `web.assets_web.min.css` contains compressed frontend assets
3. **Translation System**: Prefetch mechanism for translations via `/web/webclient/translations/`
4. **WebClient Architecture**: `o_action_manager` div handles view rendering through JS
5. **Real-time Features**: Presence of `o-mail-ChatWindowContainer` indicates discuss module integration
```