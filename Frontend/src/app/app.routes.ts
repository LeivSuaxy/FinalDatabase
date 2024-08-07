import { Routes } from '@angular/router';
import {ViewsComponent} from "./views/views.component";
import {StockComponent} from "./views/stock/stock.component";
import {FormComponent} from "./views/form/form.component";
import {PostcarComponent} from "./admin/tables/product_table/postcar/postcar.component";
import {RegistroComponent} from "./views/registro/registro.component";
import { AdminComponent } from './admin/admin.component';
import { TablesComponent } from './admin/tables/tables.component';
import { Employee_tableComponent } from './admin/tables/employee_table/employee_table.component';
import { Inventory_tableComponent } from './admin/tables/inventory_table/inventory_table.component';
import { Product_tableComponent } from './admin/tables/product_table/product_table.component';
import { Post_inventoryComponent } from './admin/tables/inventory_table/post_inventory/post_inventory.component';
import { AboutComponent } from './views/about/about.component';
import { ContactComponent } from './views/contact/contact.component';
import { AuthGuardService } from './authGuard.service';
import { Post_employeeComponent } from './admin/tables/employee_table/post_employee/post_employee.component';
import { Warehouse_tableComponent } from './admin/tables/warehouse_table/warehouse_table.component';
import { Post_warehouseComponent } from './admin/tables/warehouse_table/post_warehouse/post_warehouse.component';
import {Messenger_tableComponent} from "./admin/tables/messenger_table/messenger_table.component";
import {Post_messengerComponent} from "./admin/tables/messenger_table/post_messenger/post_messenger.component";
import {Purchase_tableComponent} from "./admin/tables/purchase_table/purchase_table.component";

export const routes: Routes = [
  { path: '', component: ViewsComponent, canActivate: [AuthGuardService] },
  { path: 'main', component: ViewsComponent, canActivate: [AuthGuardService] },
  { path: 'stock', component: StockComponent, canActivate: [AuthGuardService] },
  { path: 'login', component: FormComponent },
  { path: 'stock_add', component: PostcarComponent, canActivate: [AuthGuardService] },
  { path: 'register', component: RegistroComponent },
  { path: 'admin', component: AdminComponent, canActivate: [AuthGuardService] },
  { path: 'tables', component: TablesComponent, canActivate: [AuthGuardService] },
  { path: 'tables/employee_table', component: Employee_tableComponent, canActivate: [AuthGuardService] },
  { path: 'tables/inventory_table', component: Inventory_tableComponent, canActivate: [AuthGuardService] },
  { path: 'tables/product_table', component: Product_tableComponent, canActivate: [AuthGuardService] },
  { path: 'inventory_add', component: Post_inventoryComponent, canActivate: [AuthGuardService] },
  { path: 'about', component: AboutComponent, canActivate: [AuthGuardService] },
  { path: 'contact', component: ContactComponent, canActivate: [AuthGuardService] },
  { path: 'employee_add', component: Post_employeeComponent, canActivate: [AuthGuardService]},
  { path: 'tables/warehouse_table', component: Warehouse_tableComponent, canActivate: [AuthGuardService]},
  { path: 'warehouse_add', component: Post_warehouseComponent, canActivate: [AuthGuardService]},
  { path: 'tables/messenger_table', component: Messenger_tableComponent, canActivate: [AuthGuardService]},
  { path: 'messenger_add', component: Post_messengerComponent, canActivate: [AuthGuardService]},
  { path: 'tables/purchase_order_table', component: Purchase_tableComponent, canActivate: [AuthGuardService]},
];
