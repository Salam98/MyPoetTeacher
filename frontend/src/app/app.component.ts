import { Component, ElementRef, HostListener, inject, ViewChild } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import * as variable from "../app/appVariable";
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { PromptService } from './prompt.service';
import { HttpClient } from '@angular/common/http';
import { ResponseMessageComponent } from './response-message/response-message.component';
import { timeout } from 'rxjs';


interface ChatMessage {
  message: string;
  isLoading: boolean;
  isResponseMesage: boolean;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, FormsModule, CommonModule, ResponseMessageComponent],
  providers: [PromptService],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  //mesages array
  chatMessages: ChatMessage[] = [];

  //some needed variables
  title = 'my_poet_teacher';
  textInput = '';
  layoutStyle = '';
  btnClicked = '';
  firstLine = '';
  secondLine = '';
  thirdLine = '';

  display: HTMLImageElement
  el: ElementRef<HTMLElement>;
  @ViewChild('textarea') textarea!: ElementRef<HTMLTextAreaElement>;


  constructor(element: ElementRef<HTMLElement>) {
    this.el = element;
    this.display = this.el.nativeElement.querySelector('.poem-display')!;

  }
  http = inject(HttpClient);

  onTextareaChange() {
    this.textarea.nativeElement.setAttribute('style', `height:28px;`);
    this.textarea.nativeElement.setAttribute('style', `height:${this.textarea.nativeElement.scrollHeight}px;`);

  }



  ngAfterViewInit() {
    this.display = this.el.nativeElement.querySelector('.poem-display')!;

  }
  generateText() {

    //check if client has clicked the send button 
    if (this.btnClicked != 'circle') {
      this.btnClicked = 'round';
      setTimeout(() => {
        this.btnClicked = 'circle';
        this.updateChat();

      }, 500);
    } else {

      this.updateChat();

    }

  }


  updateChat() {

    const url = variable.url;
    let ques = this.textInput
    let request = this.http.post(url, { ques });
    let text = ""
    let x = ''
    const myQuestion: ChatMessage = { message: this.textInput, isLoading: false, isResponseMesage: false }
    this.display.scrollTo(0, this.display.scrollHeight)
    this.textInput = '';
    setTimeout(() => {
      this.textarea.nativeElement.setAttribute('style', `height:28px;`);
    }, 0);

    this.chatMessages.push(myQuestion)
    this.display.scrollTo(0, this.display.scrollHeight)
    const newChatMessage: ChatMessage = { message: '', isLoading: true, isResponseMesage: true }
    this.chatMessages.push(newChatMessage)

    request.subscribe((response: any) => {
      newChatMessage.isLoading = false;
      text = response['response'];
      let IntervalId = setInterval(() => {
        if (text.length === 0) {
          clearInterval(IntervalId);
        }
        else {
          x += text.substring(0, 1)
          text = text.substring(1)
          newChatMessage.message = x
          this.display.scrollTo(0, this.display.scrollHeight)
        }

      }, 25);
    },(error:any)=>{
      newChatMessage.isLoading = false;
      newChatMessage.message="حدثت مشكلة في الإتصال"
    });

  }
  @HostListener('window:load')
  onLoad() {
    let pageTitleSection = this.el.nativeElement.querySelector('.page-title')!;
    let promptSection = this.el.nativeElement.querySelector('.prompt-section')!;
    this.layoutStyle = pageTitleSection.clientHeight + promptSection.clientHeight > window.innerHeight ? 'fit-content' : '';
    let startText: String[] = ['فاسألْ عن النحوِ، هنا دُرَرٌ تُنسَجُ', ' .. ', 'بذكاءِ فنٍّ، يشرحُ كلَّ ما تَطلبُ']
    let index = 0
    let IntervalId = setInterval(() => {
      if (index === 2 && startText[index].length === 0) {
        index = 0
        clearInterval(IntervalId);

      }
      else if (startText[index].length === 0) {
        index++
      }
      else {
        switch (index) {
          case 0:

            this.firstLine += startText[index].substring(0, 1);
            startText[index] = startText[index].substring(1);

            break;
          case 1:

            this.secondLine += startText[index].substring(0, 1);
            startText[index] = startText[index].substring(1);

            break;
          case 2:

            this.thirdLine += startText[index].substring(0, 1);
            startText[index] = startText[index].substring(1);
            break;

          default:
            break;
        }


      }

    }, 25);

  }


  @HostListener('window:resize', ['$event'])
  onResize(event: any) {
    let pageTitleSection = this.el.nativeElement.querySelector('.page-title')!;
    let promptSection = this.el.nativeElement.querySelector('.prompt-section')!;
    this.layoutStyle = pageTitleSection.clientHeight + promptSection.clientHeight > window.innerHeight ? 'fit-content' : '';

  }

  textEnter(event:Event){
    event.preventDefault();
    this.textInput.trim().length !== 0 && this.generateText()
  }

  recommendation(event: Event) {
    this.textInput = (<HTMLElement>event.target).innerText
    this.generateText();
  }

}
