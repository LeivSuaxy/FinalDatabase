import { Component } from '@angular/core';
import {FormsModule} from "@angular/forms";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatSelectModule} from '@angular/material/select';
import {MatInputModule} from '@angular/material/input';
import {MatIconModule} from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { Router, RouterLink } from '@angular/router';
import {MatCheckboxModule} from '@angular/material/checkbox';

@Component({
  selector: 'app-post_messenger',
  standalone: true,
  imports: [
    FormsModule,
    HttpClientModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    MatIconModule,
    MatButtonModule,
    RouterLink,
    MatCheckboxModule
  ],
  templateUrl: './post_messenger.component.html',
  styleUrl: './post_messenger.component.css'
})
export class Post_messengerComponent {
  employee_ci? : string;
  vehicle? : string;
  salary_per_km? : number;


  constructor(private http : HttpClient, private router: Router) {
  }

  async posMethod(again: boolean): Promise<void> {
    let url = 'http://localhost:8000/api/admin/insert_messenger/';
    const formData = new FormData();
    formData.append('employee_ci', this.employee_ci ? this.employee_ci : '');
    formData.append('vehicle', this.vehicle ? this.vehicle : '');
    formData.append('salary_per_km', this.salary_per_km?.toString() ?? '');

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log(data);
      this.employee_ci = this.vehicle = this.salary_per_km = undefined;

      if (!again) {
        this.cancel();
      } else {
        this.employee_ci = "";
        this.vehicle = "";
        this.salary_per_km = undefined;
      }
    } catch (error) {
      console.error('There was a problem with your fetch operation:', error);
    }
  }

  cancel(): void {
    this.router.navigate(['/tables/messenger_table']);
  }
}
