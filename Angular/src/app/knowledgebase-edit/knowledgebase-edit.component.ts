import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ChecklistService } from '../services/checklist.service'
import { KnowledgebaseService } from '../services/knowledgebase.service'

import { QuestionsService } from '../services/questions.service'
import { AppSettings } from '../globals';
import * as JWT from 'jwt-decode';
import { Knowledgebase } from '../models/knowledgebase';


@Component({
  selector: 'app-knowledgebase-edit',
  templateUrl: './knowledgebase-edit.component.html',
  providers: [ChecklistService, QuestionsService]
})
export class KnowledgebaseEditComponent implements OnInit {

  constructor(
    private _knowledgeService: KnowledgebaseService,
    private route: ActivatedRoute,
    private router: Router,
  ) { }

  public canEdit: string;
  public knowledgebaseID: number;
  public return: boolean;
  public errors: string[];
  public error: string;
  public IdFromUrl: number;
  public title: string;
  public content: string;
  knowledgebaseItems: Knowledgebase[];

  ngOnInit() {

    this.route.params.subscribe(params => {
      this.IdFromUrl = params['id'];
    });

    if (AppSettings.AUTH_TOKEN) {
      const decodedJWT = JWT(AppSettings.AUTH_TOKEN);
      this.canEdit = decodedJWT.privilege.includes('edit');
    }
    setTimeout(() => {
      this.getKnowledgebaseItem();
    }, 500);
  }

  updateKnowledgebaseItem() {

    this.errors = [];
    this.return = true;

    if (!this.title) { this.errors.push('Title was left empty'); this.return = false; }
    if (!this.content) { this.errors.push('Content was left empty'); this.return = false; }
    if (this.return == false) { return; }

    this.errors = [];
    this._knowledgeService.updateKnowledgebaseItem(Number(this.IdFromUrl), this.title, this.content)
      .subscribe(
        () => this.back(),
        () => this.errors.push('Error updating checklist item, potential duplicate or incorrect checklist ID (1.2, 1.2, 2.1, etc)')
      );

      this._knowledgeService.getKnowledgeBase().subscribe(requestData => this.knowledgebaseItems = requestData,
        err => this.error = 'Error getting knowledge items, contact the administrator!'
      );
    
      this.router.navigate(['/knowledgebase']);
  }

  getKnowledgebaseItem() {
    this._knowledgeService.getKnowledgebaseItem(this.IdFromUrl).subscribe(
      knowledgebaseItems => {
        this.title = knowledgebaseItems['title']
        this.content = knowledgebaseItems['content']
      },
      err => this.error = 'Error getting knowledge items, contact the administrator!'
    );
  }

  back() {
    this.router.navigate(['/knowledgebase']);
  }
}
