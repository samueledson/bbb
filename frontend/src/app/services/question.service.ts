import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { api } from 'src/config';

@Injectable({
	providedIn: 'root',
})
export class QuestionService {
	constructor(private _http: HttpClient) {}

	getQuestions(season: string) {
    return this._http.get(`${api.questions_program_season}/${season}`);
  }

}
