import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-response-message',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './response-message.component.html',
  styleUrl: './response-message.component.css'
})
export class ResponseMessageComponent {
  @Input() isLoading: boolean = false;

  @Input() message: String = '';

  @Input() isResponseMesage: boolean = false;


}
